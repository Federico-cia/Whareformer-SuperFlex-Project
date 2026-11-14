"""Stage ordering, deferred waiting and failure preservation; no inference."""
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from run_pipeline import run_pipeline


class PipelineTests(unittest.TestCase):
    def files(self,folder):
        root=Path(folder);(root/'inputs').mkdir()
        (root/'inputs/input_manifest.json').write_text('{}')
        (root/'config.json').write_text('{}');(root/'policy.json').write_text('{}')
        return root

    def test_stages_order_and_fresh_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.files(folder);seen=[]
            def command(args,**kwargs):
                seen.append(Path(args[1]).stem)
                target=Path(args[args.index('--output')+1]);target.mkdir()
                (target/('comparison.csv' if seen[-1]=='summarize_experiments' else 'summary.json')).write_text('{}')
                return SimpleNamespace(returncode=0)
            result=run_pipeline(root/'inputs',root/'config.json',root/'run',root/'cache',root/'policy.json',command_runner=command)
            self.assertEqual(result['status'],'completed')
            self.assertEqual(seen,['run_experiments','evaluate_experiments','summarize_experiments'])
            with self.assertRaises(FileExistsError):run_pipeline(root/'inputs',root/'config.json',root/'run',root/'cache',root/'policy.json')

    def test_waiting_does_not_run_evaluation(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.files(folder);seen=[]
            def command(args,**kwargs):seen.append(args);return SimpleNamespace(returncode=2)
            result=run_pipeline(root/'inputs',root/'config.json',root/'run',root/'cache',root/'policy.json',command_runner=command)
            self.assertEqual(result['status'],'waiting_for_results');self.assertEqual(len(seen),1)

    def test_evaluation_failure_stops_comparison(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.files(folder);codes=iter([0,1])
            def command(args,**kwargs):
                code=next(codes)
                if code==0:
                    target=Path(args[args.index('--output')+1]);target.mkdir();(target/'summary.json').write_text('{}')
                return SimpleNamespace(returncode=code)
            result=run_pipeline(root/'inputs',root/'config.json',root/'run',root/'cache',root/'policy.json',command_runner=command)
            self.assertEqual(result['status'],'failed');self.assertEqual(len(result['stages']),2)


if __name__=='__main__':unittest.main()
