import io
from pathlib import Path
import tarfile
import tempfile
import unittest
import drive_delivery as delivery


class DeliveryTests(unittest.TestCase):
    def test_archive_roundtrip_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source';source.mkdir();(source/'data.bin').write_bytes(b'original\x00data'*100)
            receipt=delivery.pack_directory(source,root/'block.tar','0004')
            checked=delivery.verify_archive(root/'block.tar',root/'restored')
            self.assertEqual(receipt['sha256'],checked['archive_sha256'])
            self.assertEqual((root/'restored/0004/data.bin').read_bytes(),(source/'data.bin').read_bytes())
            with self.assertRaises(FileExistsError):delivery.verify_archive(root/'block.tar',root/'restored')

    def test_unsafe_member_and_symlink_rejected(self):
        for name,kind in [('../escape',tarfile.REGTYPE),('safe',tarfile.SYMTYPE)]:
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/'bad.tar'
                with tarfile.open(p,'w') as tar:
                    info=tarfile.TarInfo(name);info.type=kind;info.linkname='outside';tar.addfile(info)
                with self.assertRaises(ValueError):delivery.verify_archive(p)

    def test_locked_source_and_output_inside_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'source';source.mkdir();(source/'.retention.lock').touch()
            with self.assertRaises(ValueError):delivery.pack_directory(source,Path(tmp)/'archive.tar','0004')
            with self.assertRaises(ValueError):delivery.pack_directory(source,source/'archive.tar','0004')

    def test_auth_missing_never_uploads(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError,'AUTHORIZATION_REQUIRED'):
                delivery.Drive('unused',Path(tmp)/'missing.conf')

    def test_relative_paths_reject_traversal_and_windows_paths(self):
        for name in ('../bad','/bad','C:/bad','a\\b'):
            with self.assertRaises(ValueError):delivery.safe_relative(name)


if __name__=='__main__':unittest.main()
