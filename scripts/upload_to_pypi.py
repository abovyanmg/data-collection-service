#!/usr/bin/env python3
"""
Upload dist/* to PyPI with increased timeout (for slow/unstable networks).

Usage (one line, paste your token at the end):
  python scripts/upload_to_pypi.py __token__ pypi-ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН

Or via env:
  set TWINE_USERNAME=__token__
  set TWINE_PASSWORD=pypi-...
  python scripts/upload_to_pypi.py
"""
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

REPO_URL = "https://upload.pypi.org/legacy/"
TIMEOUT = 300  # seconds (5 min) — increase if needed

def main():
    if len(sys.argv) >= 3:
        username, password = sys.argv[1], sys.argv[2]
    else:
        username = os.environ.get("TWINE_USERNAME")
        password = os.environ.get("TWINE_PASSWORD")
    if not username or not password:
        print("Usage: python scripts/upload_to_pypi.py __token__ pypi-ВАШ_ТОКЕН", file=sys.stderr)
        print("   or set TWINE_USERNAME and TWINE_PASSWORD", file=sys.stderr)
        sys.exit(1)

    base = Path(__file__).resolve().parent
    dist = (base / "dist").resolve()
    if not dist.is_dir():
        dist = (base.parent / "dist").resolve()  # repo: scripts/ -> project root
    if not dist.is_dir():
        print("Folder dist/ not found. Run: python -m build", file=sys.stderr)
        sys.exit(1)

    files = list(dist.glob("*.whl")) + list(dist.glob("*.tar.gz"))
    if not files:
        print("No .whl or .tar.gz in dist/. Run: python -m build", file=sys.stderr)
        sys.exit(1)

    auth = (username, password)
    for path in files:
        print(f"Uploading {path.name} (timeout={TIMEOUT}s)...")
        with open(path, "rb") as f:
            data = f.read()
        try:
            r = requests.post(
                REPO_URL,
                auth=auth,
                files={"file": (path.name, data, "application/octet-stream")},
                timeout=TIMEOUT,
            )
        except requests.exceptions.Timeout:
            print(f"  TIMEOUT after {TIMEOUT}s. Try another network (mobile, no VPN) or increase TIMEOUT in script.", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}", file=sys.stderr)
            sys.exit(1)

        if r.status_code in (200, 201):
            print(f"  OK {r.status_code}")
        else:
            print(f"  HTTP {r.status_code}: {r.text[:500]}", file=sys.stderr)
            sys.exit(1)

    print("Done.")

if __name__ == "__main__":
    main()
