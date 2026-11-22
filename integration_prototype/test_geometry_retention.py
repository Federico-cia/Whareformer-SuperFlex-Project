"""Safety boundaries for destructive lifecycle changes; actual geometry is checked on HPC."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import geometry_retention as retention


class RetentionSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'geometry' / '0000'
        self.root.mkdir(parents=True)

    def artifact(self, name, payload=b'retained scientific data'):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(payload)
        return dict(path=name, sha256=hashlib.sha256(payload).hexdigest())

    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError): retention.bound(self.root, '../../important_file')

    def test_corrupt_prerequisite_rejected(self):
        info = self.artifact('clouds_da/one/points.npz')
        (self.root / info['path']).write_bytes(b'changed')
        with self.assertRaises(ValueError): retention.checked(self.root, info)

    def test_no_compaction_without_export(self):
        with self.assertRaises(ValueError): retention.compact(self.root, 'absent-proof', apply=True)

    def test_no_compaction_without_matching_replay_proof(self):
        retention.save(self.root/'observations.json', [])
        proof = self.root/'proof.json'
        retention.save(proof, dict(status='failed', provenance={}))
        with self.assertRaises(ValueError): retention.compact(self.root, proof, apply=True)
        self.assertFalse((self.root/retention.LEDGER).exists())

    def test_only_canonical_derived_paths_can_be_deleted(self):
        info = self.artifact('clouds_da/one/points.npz')
        report = dict(artifacts=dict(surface=info, parameters=info), signature='same')
        with self.assertRaises(ValueError): retention.entry_for(self.root, 'da', 'one', report, info, 42, 'surface')

    def setup_absent(self):
        params = self.artifact('superflex_da/one/shape_parameters.npz')
        cloud = self.artifact('clouds_da/one/points.npz')
        info = dict(path='superflex_da/one/reconstruction.ply', sha256='original-surface-hash')
        retention.save(self.root/retention.LEDGER, dict(provenance={'test':1}, entries={info['path']:dict(
            sha256=info['sha256'], stage_signature='scientific-signature', parameters=params, cloud=cloud)}))
        folder = self.root/'superflex_da/one'
        retention.save(folder/'report.json', dict(signature='scientific-signature', status='ready', artifacts={'surface':info,'parameters':params}))
        return folder, info, params, cloud

    def test_registered_absence_is_accepted_without_fake_file(self):
        folder, info, _, _ = self.setup_absent()
        module = SimpleNamespace()
        with patch.object(retention, 'recipe_provenance', return_value={'test':1}):
            retention.install_cache_adapter(module, self.root)
        result = module.cached(folder, 'scientific-signature')
        self.assertEqual(result['status'], 'ready')
        self.assertFalse((self.root/info['path']).exists())
        with self.assertRaises(ValueError): module.cached(folder, 'changed-scientific-signature')

    def test_missing_retained_geometry_still_fails(self):
        folder, _, _, cloud = self.setup_absent()
        (self.root/cloud['path']).unlink()
        module = SimpleNamespace()
        with patch.object(retention, 'recipe_provenance', return_value={'test':1}): retention.install_cache_adapter(module, self.root)
        with self.assertRaises((ValueError, FileNotFoundError)): module.cached(folder, 'scientific-signature')

    def test_unregistered_absence_still_fails(self):
        folder, _, _, _ = self.setup_absent()
        ledger = retention.read(self.root/retention.LEDGER);ledger['entries']={}
        retention.save(self.root/retention.LEDGER,ledger)
        module=SimpleNamespace()
        with patch.object(retention, 'recipe_provenance', return_value={'test':1}): retention.install_cache_adapter(module, self.root)
        with self.assertRaises(ValueError): module.cached(folder, 'scientific-signature')


if __name__ == '__main__': unittest.main()
