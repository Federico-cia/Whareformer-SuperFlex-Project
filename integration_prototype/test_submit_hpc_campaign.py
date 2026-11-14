import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from submit_hpc_campaign import submit,schedule_summary


class SubmissionTests(unittest.TestCase):
    def directory(self,root):
        path=Path(root);(path/'inputs').mkdir();(path/'inputs/selection.json').write_text('{}')
        (path/'campaign.json').write_text(json.dumps(dict(variants=dict(cpu=[{},{}],gpu=[{}]))))
        for lane in ['cpu','gpu']:
            (path/(lane+'.sbatch')).write_text('#!/bin/bash\n#SBATCH --time=00:45:00\n#SBATCH --array=0-2%2\npython -u runtime/integration_prototype/hpc_campaign.py variant --task "$TASK" --lane '+lane+' --index "$SLURM_ARRAY_TASK_ID"\n')
        return path

    def test_no_submission_before_success(self):
        with tempfile.TemporaryDirectory() as root:
            path=self.directory(root)
            with patch('submit_hpc_campaign.subprocess.check_output',return_value='12|RUNNING|0:0|\n') as check:
                with self.assertRaises(RuntimeError):submit(path,'12')
            self.assertEqual(check.call_count,1)
            self.assertFalse((path/'submitted_jobs.json').exists())

    def test_explicit_dependencies_and_existing_receipt_guard(self):
        with tempfile.TemporaryDirectory() as root:
            path=self.directory(root)
            values=['12|COMPLETED|0:0|\n']
            for job in range(20,24):values+=['account\n',str(job)+'\n']
            with patch('submit_hpc_campaign.subprocess.check_output',side_effect=values):record=submit(path,'12')
            self.assertEqual(record['jobs']['geometry']['dependency'],'afterok:12')
            self.assertEqual(record['jobs']['cpu']['dependency'],'afterok:21')
            self.assertNotIn('summarize',record['jobs'])
            self.assertNotIn('#SBATCH --array',(path/'cpu_group.sbatch').read_text())
            with patch('submit_hpc_campaign.subprocess.check_output',side_effect=['account\n','24\n']):record=schedule_summary(path)
            self.assertEqual(record['jobs']['summarize']['dependency'],'afterany:22:23')
            self.assertEqual(schedule_summary(path),record)
            self.assertEqual(json.loads((path/'submitted_jobs.json').read_text()),record)
            with self.assertRaises(FileExistsError):submit(path,'12')

    def test_partial_submission_ids_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            path=self.directory(root)
            values=['12|COMPLETED|0:0|\n','account\n','20\n','account\n',RuntimeError('scheduler refused')]
            with patch('submit_hpc_campaign.subprocess.check_output',side_effect=values):
                with self.assertRaises(RuntimeError):submit(path,'12')
            record=json.loads((path/'submitted_jobs.json').read_text())
            self.assertEqual(record['jobs']['geometry']['id'],'20')
            self.assertEqual(record['submission_error']['stage'],'build')


if __name__=='__main__':unittest.main()
