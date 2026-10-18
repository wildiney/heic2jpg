# heic2jpg

Convert HEIC/HEIF photos (iPhone) to JPG from the terminal. Keeps EXIF and ICC profile; rotation is baked into the pixels.

## Usage

```bash
heic2jpg foto.heic                  # -> foto.jpg next to the source
heic2jpg C:\fotos -r -o C:\jpgs     # whole folder, recursive, custom output dir
heic2jpg a.heic b.heic -q 85        # JPEG quality (default 92)
heic2jpg foto.heic --overwrite      # replace existing .jpg
```

| Option | Meaning |
|---|---|
| `-o, --outdir` | output directory (default: beside source) |
| `-q, --quality` | JPEG quality, default 92 |
| `-r, --recursive` | recurse into directories |
| `--overwrite` | overwrite existing `.jpg` (default: skip) |
| `-V, --version` | print version |

Exit code is `1` if any file failed, `0` otherwise.

## Install as executable (Windows)

Builds a single-file `heic2jpg.exe` with PyInstaller and copies it to `C:\tools` (must be on `PATH`):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build.ps1
# other location: ... -File scripts\build.ps1 -InstallDir D:\bin
```

## Dev

```bash
pip install -e ".[dev]"
pytest
python -m heic2jpg foto.heic
```

## Layout

```
src/heic2jpg/   package (cli.py = logic)
entry.py        PyInstaller entry point
scripts/        build.ps1
tests/          pytest
```
