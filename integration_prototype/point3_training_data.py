"""Reader for point-2 experiments; no new distance or matcher policy imposed."""
import hashlib
import json
from pathlib import Path
import numpy as np


class AccumulatedTrainingData:
    def __init__(self, root, *, completed=False):
        self.root = Path(root).resolve()
        self.completed = completed
        name = 'examples_with_reconstructions.json' if completed else 'examples.json'
        self.rows = json.loads((self.root / name).read_text())
        self.by_key = {r['observation_key']: r for r in self.rows}
        if len(self.rows) != len(self.by_key):
            raise ValueError('Duplicate training observation')

    def feature(self, spec):
        if spec is None:
            return None
        path = (self.root / spec['path']).resolve()
        if (not path.is_relative_to(self.root)
                or hashlib.sha256(path.read_bytes()).hexdigest() != spec['sha256']):
            raise ValueError('Feature checksum/path mismatch')
        with np.load(path, allow_pickle=False) as z:
            if bool(z['completed_by_superflex']) != self.completed:
                raise ValueError('Observed/completed representation mismatch')
            features = {k: z[k].copy() for k in ('points', 'd2', 'spectrum')}
            if not all(np.isfinite(v).all() for v in features.values()):
                raise ValueError('Nonfinite feature')
            return features

    def example(self, key):
        row = self.by_key[key]
        query = self.feature(row.get('query_reconstruction') if self.completed else row['query'])
        memories, available = [], []
        for candidate in row['candidates']:
            memory = candidate['memory']
            if memory is not None and memory['last_update_frame'] >= row['frame_index']:
                raise ValueError('Current/future geometry cannot enter candidate memory')
            spec = candidate.get('reconstruction') if self.completed else (None if memory is None else memory['points'])
            if self.completed and spec and (str(spec['track_id']) != str(candidate['track_id'])
                    or spec['last_update_frame'] >= row['frame_index']):
                raise ValueError('Reconstruction scope or causality mismatch')
            feature = self.feature(spec)
            memories.append(feature)
            available.append(query is not None and feature is not None)
        with np.load(self.root / 'training_inputs.npz', allow_pickle=False) as z:
            numerical = z[row['numerical_input_key']].copy()
            label = z[row['numerical_label_key']].copy()
        return dict(observation_key=key, numerical_input=numerical, original_label=label,
                    target_class=row['target_class'], candidate_track_ids=row['candidate_track_ids'],
                    query=query, candidate_memories=memories,
                    geometry_available=np.asarray(available, dtype=bool), new_track_class=0,
                    representation='superflex_completed' if self.completed else 'observed_accumulated')
