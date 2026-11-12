"""Portable, staged RGB/mask -> geometry pipeline. Neural stages require CUDA.

Run ``python -m shape_tools.pipeline --help``. Paths in manifests are relative
to that manifest; artifact paths are relative to the output directory.
"""

import argparse
import hashlib
import importlib
import json
import os
import re
import time
from pathlib import Path

import numpy as np

from .comparison import file_hash
from .geometry import backproject, prepare_superflex_input, validate_points


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    os.replace(tmp, path)


def source_hashes():
    return {
        name: file_hash(Path(__file__).parent / name)
        for name in ("pipeline.py", "geometry.py", "comparison.py")
    }


def backend_provenance(package):
    import torch

    module = importlib.import_module(package)
    root = Path(module.__file__).parent if module.__file__ else Path(next(iter(module.__path__)))
    return dict(
        torch=torch.__version__,
        cuda=torch.version.cuda,
        package=package,
        version=getattr(module, "__version__", None),
        sources={p.relative_to(root).as_posix(): file_hash(p) for p in sorted(root.rglob("*.py"))},
    )


def read_manifest(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("schema_version") != 1 or not data.get("observations"):
        raise ValueError("Expected schema_version=1 and nonempty observations")
    seen = set()
    for row in data["observations"]:
        for key in ("observation_key", "video", "frame_index", "rgb", "mask", "category"):
            if key not in row:
                raise ValueError(f"Missing {key}")
        if row["observation_key"] in seen:
            raise ValueError("Duplicate observation key")
        seen.add(row["observation_key"])
        if not isinstance(row["frame_index"], int) or row["frame_index"] < 0:
            raise ValueError("frame_index must be a nonnegative integer")
        for key in ("rgb", "mask"):
            row[key] = str((path.parent / row[key]).resolve())
    return data


def item_id(row):
    return hashlib.sha256(row["observation_key"].encode()).hexdigest()[:24]


def artifact(output, path):
    return dict(path=path.relative_to(output).as_posix(), sha256=file_hash(path))


def cached(folder, signature):
    report = folder / "report.json"
    if not report.exists():
        return None
    result = json.loads(report.read_text())
    if result["signature"] != signature:
        raise ValueError(f"Incompatible resume: {folder}; use a new output directory")
    if result["status"] == "ready":
        for value in result["artifacts"].values():
            path = folder / Path(value["path"]).name
            if not path.is_file() or file_hash(path) != value["sha256"]:
                raise ValueError(f"Corrupt cached artifact: {path}")
    return result


def run_item(output, folder, signature, producer):
    previous = cached(folder, signature)
    if previous is not None:
        return previous
    folder.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    try:
        files, details = producer(folder)
        result = dict(
            status="ready", artifacts={k: artifact(output, v) for k, v in files.items()}, **details
        )
    except (ValueError, RuntimeError, OSError) as error:
        result = dict(
            status="failed", artifacts={}, error_type=type(error).__name__, error=str(error)
        )
    result.update(signature=signature, elapsed_seconds=time.perf_counter() - started)
    save_json(folder / "report.json", result)
    return result


def image_inputs(row):
    from PIL import Image

    rgb = np.asarray(Image.open(row["rgb"]).convert("RGB"))
    mask = np.asarray(Image.open(row["mask"]))
    if mask.ndim != 2 or mask.shape != rgb.shape[:2]:
        raise ValueError("Mask must be single-channel at exactly the RGB resolution")
    values = set(np.unique(mask).tolist())
    if not values <= {0, 1, 255}:
        raise ValueError("Mask must encode a single object using 0 and 1/255")
    return rgb, mask > 0


def neural_model(source, config):
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("Neural stages require an assigned CUDA GPU")
    torch.manual_seed(config.get("seed", 42))
    if source == "da":
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation

        opts = dict(revision=config["revision"], local_files_only=True)
        processor = AutoImageProcessor.from_pretrained(config["model"], **opts)
        model = AutoModelForDepthEstimation.from_pretrained(config["model"], **opts).eval().cuda()

        def infer(rgb):
            x = torch.from_numpy(rgb.copy()).permute(2, 0, 1).float() / 255
            inputs = processor(images=[x], return_tensors="pt", do_rescale=False).to("cuda")
            depth = model(**inputs).predicted_depth.unsqueeze(1)
            depth = torch.nn.functional.interpolate(
                depth, size=rgb.shape[:2], mode="bicubic", align_corners=False
            )
            return {"depth": torch.relu(depth)[0, 0].cpu().numpy()}
    else:
        from moge.model.v2 import MoGeModel

        path = Path(config["checkpoint"])
        if file_hash(path) != config["checkpoint_sha256"]:
            raise ValueError("MoGE checkpoint checksum mismatch")
        weights = torch.load(path, map_location="cpu", weights_only=True)
        model = MoGeModel(**weights["model_config"])
        model.load_state_dict(weights["model"], strict=True)
        model.eval().cuda()

        def infer(rgb):
            x = torch.from_numpy(rgb.copy()).permute(2, 0, 1).float().cuda() / 255
            result = model.infer(x, **config["settings"])
            return {key: value.cpu().numpy() for key, value in result.items()}

    return infer


def inference(data, output, source, config):
    import torch

    infer = neural_model(source, config[source])
    backend = backend_provenance("transformers" if source == "da" else "moge")
    save_json(output / f"{source}_backend.json", backend)
    results = {}
    for row in data["observations"]:
        rgb_hash = file_hash(row["rgb"])
        signature = digest(
            dict(rgb=rgb_hash, config=config[source], code=source_hashes(), backend=backend)
        )
        folder = output / source / rgb_hash[:24]

        def produce(dest, row=row, rgb_hash=rgb_hash):
            from PIL import Image

            rgb = np.asarray(Image.open(row["rgb"]).convert("RGB"))
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.synchronize()
            with torch.inference_mode():
                arrays = infer(rgb)
            torch.cuda.synchronize()
            if source == "da" and (
                arrays["depth"].shape != rgb.shape[:2] or not np.isfinite(arrays["depth"]).all()
            ):
                raise ValueError("Invalid DA depth")
            path = dest / "prediction.npz"
            np.savez_compressed(path, **arrays)
            return {"prediction": path}, dict(
                rgb_sha256=rgb_hash,
                torch=torch.__version__,
                gpu=torch.cuda.get_device_name(0),
                peak_allocated_bytes=torch.cuda.max_memory_allocated(),
            )

        results[item_id(row)] = run_item(output, folder, signature, produce)
    save_json(output / f"{source}_index.json", results)


def clouds(data, output, config):
    indices = {s: json.loads((output / f"{s}_index.json").read_text()) for s in config["sources"]}
    results = {s: {} for s in config["sources"]}
    for row in data["observations"]:
        key = item_id(row)
        upstream = {s: indices[s][key] for s in config["sources"]}
        signature = digest(
            dict(
                row=row,
                rgb=file_hash(row["rgb"]),
                mask=file_hash(row["mask"]),
                upstream=upstream,
                config=config["clouds"],
                code=source_hashes(),
            )
        )
        for source in config["sources"]:

            def produce(dest, row=row, upstream=upstream, source=source):
                rgb, mask = image_inputs(row)
                maps, valid = {}, {}
                for s, info in upstream.items():
                    if info["status"] != "ready":
                        continue
                    pred = info["artifacts"]["prediction"]
                    path = output / pred["path"]
                    if file_hash(path) != pred["sha256"]:
                        raise ValueError("Upstream prediction checksum mismatch")
                    with np.load(path, allow_pickle=False) as arrays:
                        maps[s] = (
                            backproject(arrays["depth"], row["intrinsics"])
                            if s == "da"
                            else arrays["points"].copy()
                        )
                        good = (
                            np.ones(mask.shape, bool) if s == "da" else arrays["mask"].astype(bool)
                        )
                    if maps[s].shape != (*mask.shape, 3) or good.shape != mask.shape:
                        raise ValueError("Geometry and mask resolution mismatch")
                    valid[s] = mask & good & np.isfinite(maps[s]).all(-1) & (maps[s][..., 2] > 0)
                if source not in maps:
                    raise ValueError("Source inference unavailable")
                if config["clouds"]["pixel_policy"] == "common":
                    if len(maps) != len(config["sources"]):
                        raise ValueError("Common-pixel policy requires all sources")
                    keep = np.logical_and.reduce(list(valid.values()))
                else:
                    keep = valid[source]
                if keep.sum() < config["clouds"]["minimum_points"]:
                    raise ValueError("Insufficient valid object pixels")
                points = validate_points(maps[source][keep])
                yy, xx = np.nonzero(keep)
                path = dest / "points.npz"
                np.savez_compressed(
                    path, camera_points=points, colors=rgb[keep], pixels_xy=np.stack([xx, yy], -1)
                )
                return {"points": path}, dict(
                    mask_pixels=int(mask.sum()),
                    source_valid_pixels=int(valid[source].sum()),
                    points=len(points),
                    pixel_policy=config["clouds"]["pixel_policy"],
                )

            results[source][key] = run_item(
                output, output / f"clouds_{source}" / key, signature, produce
            )
    for source, records in results.items():
        save_json(output / f"clouds_{source}_index.json", records)


def superflex(data, output, config):
    import torch
    from omegaconf import OmegaConf
    from superflex.data.dataloader import denormalize_outdict, denormalize_points
    from superflex.superflex import SuperFlex
    from superflex.utils.predictions_handler import PredictionHandler

    cfg = config["superflex"]
    for name in ("checkpoint", "config"):
        if file_hash(cfg[name]) != cfg[f"{name}_sha256"]:
            raise ValueError(f"SuperFlex {name} checksum mismatch")
    if not torch.cuda.is_available():
        raise RuntimeError("SuperFlex requires an assigned CUDA GPU")
    torch.manual_seed(cfg["seed"])
    model = SuperFlex(OmegaConf.load(cfg["config"]).superflex).cuda().eval()
    # Authors' trusted checkpoint contains configuration in addition to tensors.
    model.load_state_dict(
        torch.load(cfg["checkpoint"], map_location="cpu", weights_only=False)["model_state_dict"],
        strict=True,
    )
    backend = backend_provenance("superflex")
    save_json(output / "superflex_backend.json", backend)
    for source in config["sources"]:
        index = json.loads((output / f"clouds_{source}_index.json").read_text())
        results = {}
        for row in data["observations"]:
            key = item_id(row)
            upstream = index[key]
            signature = digest(
                dict(upstream=upstream, config=cfg, code=source_hashes(), backend=backend)
            )

            def produce(dest, upstream=upstream, key=key):
                if upstream["status"] != "ready":
                    raise ValueError("Cloud unavailable")
                info = upstream["artifacts"]["points"]
                path = output / info["path"]
                if file_hash(path) != info["sha256"]:
                    raise ValueError("Cloud checksum mismatch")
                with np.load(path, allow_pickle=False) as cloud:
                    original = cloud["camera_points"].copy()
                normalized, center, scale, sample = prepare_superflex_input(
                    original, seed=cfg["seed"]
                )
                np.savez_compressed(
                    dest / "input.npz",
                    sample_indices=sample,
                    normalized_points=normalized,
                    translation=center,
                    scale=scale,
                )
                x = torch.from_numpy(normalized).float().unsqueeze(0).cuda()
                torch.cuda.reset_peak_memory_stats()
                torch.cuda.synchronize()
                start = time.perf_counter()
                with torch.inference_mode():
                    prediction = model(x)
                torch.cuda.synchronize()
                elapsed = time.perf_counter() - start
                for value in prediction.values():
                    if isinstance(value, torch.Tensor) and not torch.isfinite(value).all():
                        raise ValueError("Nonfinite SuperFlex output")
                prediction = {
                    k: v.cpu() if isinstance(v, torch.Tensor) else v for k, v in prediction.items()
                }
                prediction = denormalize_outdict(
                    prediction, np.array([center]), np.array([scale]), False
                )
                restored = denormalize_points(x.cpu(), np.array([center]), np.array([scale]), False)
                handler = PredictionHandler.from_outdict(prediction, restored, [key])
                active = int((handler.exist > 0.5).sum())
                if not active:
                    raise ValueError("No active primitives at authors threshold 0.5")
                handler.save_npz(str(dest / "prediction.npz"))
                with np.load(dest / "prediction.npz", allow_pickle=False) as saved:
                    names = (
                        "scale",
                        "rotation",
                        "translation",
                        "exponents",
                        "exist",
                        "tapering",
                        "bending",
                    )
                    np.savez_compressed(
                        dest / "shape_parameters.npz", **{name: saved[name] for name in names}
                    )
                mesh = handler.get_mesh(0, resolution=30)
                validate_points(mesh.vertices)
                if not len(mesh.faces):
                    raise ValueError("Empty mesh faces")
                mesh.export(dest / "reconstruction.ply")
                return {
                    n: dest / p
                    for n, p in [
                        ("input", "input.npz"),
                        ("parameters", "shape_parameters.npz"),
                        ("diagnostic_prediction", "prediction.npz"),
                        ("surface", "reconstruction.ply"),
                    ]
                }, dict(
                    active_primitives=active,
                    forward_seconds=elapsed,
                    peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                    normalization_translation=center.tolist(),
                    normalization_scale=scale,
                )

            results[key] = run_item(
                output, output / f"superflex_{source}" / key, signature, produce
            )
        save_json(output / f"superflex_{source}_index.json", results)


def export(data, output, config):
    indices = {
        (stage, s): json.loads((output / f"{stage}_{s}_index.json").read_text())
        for stage in ("clouds", "superflex")
        for s in config["sources"]
    }
    rows = []
    for row in data["observations"]:
        record = {k: v for k, v in row.items() if k not in ("rgb", "mask")}
        record.update(
            schema_version=1,
            rgb_frame=Path(row["rgb"]).name,
            detection_idx=None,
            detection_mapping_status="unverified",
            axes="camera: X right, Y down, Z forward",
            units="model-estimated scale; physical metric accuracy unverified",
            provenance=dict(
                rgb_sha256=file_hash(row["rgb"]),
                mask_sha256=file_hash(row["mask"]),
                config_sha256=digest(config),
                code=source_hashes(),
            ),
            representations={},
        )
        for source in config["sources"]:
            for stage, suffix, asset in [
                ("clouds", "points", "points"),
                ("superflex", "superflex", "surface"),
            ]:
                info = indices[stage, source][item_id(row)]
                rep = dict(
                    status="ready" if info["status"] == "ready" else "unavailable",
                    source=source,
                    stage_signature=info["signature"],
                )
                if rep["status"] == "ready":
                    rep.update(info["artifacts"][asset])
                    rep["artifacts"] = info["artifacts"]
                else:
                    rep["reason"] = info["error"]
                record["representations"][f"{source}_{suffix}"] = rep
        rows.append(record)
    save_json(output / "observations.json", rows)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["da", "moge", "clouds", "superflex", "export"])
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = read_manifest(args.manifest)
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    if (
        not config["sources"]
        or len(set(config["sources"])) != len(config["sources"])
        or set(config["sources"]) - {"da", "moge"}
    ):
        raise ValueError("sources must contain da and/or moge once")
    if (
        config["clouds"]["pixel_policy"] not in ("common", "source")
        or config["clouds"]["minimum_points"] < 4
    ):
        raise ValueError("Invalid cloud policy")
    if "da" in config["sources"] and not re.fullmatch("[a-f0-9]{40}", config["da"]["revision"]):
        raise ValueError("Pin DA to an immutable model revision")
    for section, names in [("moge", ("checkpoint",)), ("superflex", ("checkpoint", "config"))]:
        if section in config:
            for name in names:
                config[section][name] = str(
                    (args.config.resolve().parent / config[section][name]).resolve()
                )
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    lock = output / "run.json"
    provenance = dict(
        manifest=data,
        inputs={
            row["observation_key"]: {k: file_hash(row[k]) for k in ("rgb", "mask")}
            for row in data["observations"]
        },
        config=config,
        code=source_hashes(),
    )
    signature = digest(provenance)
    if lock.exists() and json.loads(lock.read_text())["signature"] != signature:
        raise ValueError("Run inputs/configuration/code changed; use a new output directory")
    save_json(lock, dict(signature=signature, **provenance))
    if args.stage in ("da", "moge"):
        if args.stage not in config["sources"]:
            raise ValueError("Source disabled")
        inference(data, output, args.stage, config)
    else:
        {"clouds": clouds, "superflex": superflex, "export": export}[args.stage](
            data, output, config
        )


if __name__ == "__main__":
    main()
