from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

from heic2jpg.cli import main

register_heif_opener()


def make_heic(path: Path):
    Image.new("RGB", (32, 16), (200, 30, 30)).save(path, "HEIF")


def test_converts_file(tmp_path):
    src = tmp_path / "a.heic"
    make_heic(src)
    assert main([str(src)]) == 0
    assert Image.open(tmp_path / "a.jpg").size == (32, 16)


def test_skips_existing_without_overwrite(tmp_path):
    src = tmp_path / "a.heic"
    make_heic(src)
    (tmp_path / "a.jpg").write_bytes(b"keep")
    main([str(src)])
    assert (tmp_path / "a.jpg").read_bytes() == b"keep"


def test_recursive_outdir(tmp_path):
    (tmp_path / "sub").mkdir()
    make_heic(tmp_path / "sub" / "b.HEIC")
    out = tmp_path / "out"
    main([str(tmp_path), "-r", "-o", str(out)])
    assert (out / "b.jpg").exists()
