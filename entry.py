"""PyInstaller entry point (absolute import so the frozen exe works)."""
import sys

from heic2jpg.cli import main

if __name__ == "__main__":
    sys.exit(main())
