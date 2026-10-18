"""Convert .heic/.heif files to .jpg.

Usage:
    heic2jpg <file|dir> [...] [-o OUTDIR] [-q QUALITY] [-r] [--overwrite]
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

from . import __version__

register_heif_opener()

EXTS = {".heic", ".heif"}


def collect(paths, recursive):
    for p in paths:
        if p.is_dir():
            it = p.rglob("*") if recursive else p.glob("*")
            yield from (f for f in sorted(it) if f.suffix.lower() in EXTS)
        elif p.suffix.lower() in EXTS:
            yield p
        else:
            print(f"skip (not heic): {p}", file=sys.stderr)


def convert(src, outdir, quality, overwrite):
    dst = (outdir or src.parent) / (src.stem + ".jpg")
    if dst.exists() and not overwrite:
        print(f"skip (exists): {dst}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        exif = im.info.get("exif")
        icc = im.info.get("icc_profile")
        im = ImageOps.exif_transpose(im)  # bake rotation into pixels
        if im.mode != "RGB":
            im = im.convert("RGB")
        kw = {"quality": quality, "optimize": True}
        if icc:
            kw["icc_profile"] = icc
        if exif:
            # orientation already applied; reset tag to avoid double rotation
            exif_obj = Image.Exif()
            exif_obj.load(exif)
            exif_obj[0x0112] = 1
            kw["exif"] = exif_obj.tobytes()
        im.save(dst, "JPEG", **kw)
    print(f"ok: {src} -> {dst}")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="heic2jpg", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("-o", "--outdir", type=Path)
    ap.add_argument("-q", "--quality", type=int, default=92)
    ap.add_argument("-r", "--recursive", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args(argv)

    files = list(collect(a.inputs, a.recursive))
    if not files:
        sys.exit("no heic files found")
    done = fail = 0
    for f in files:
        try:
            done += convert(f, a.outdir, a.quality, a.overwrite)
        except Exception as e:
            fail += 1
            print(f"FAIL: {f}: {e}", file=sys.stderr)
    print(f"converted {done}/{len(files)}, failed {fail}")
    return 1 if fail else 0
