#!/usr/bin/env python3
"""
Uploads documentation into Algolia.
Points to .github/scripts/sync_algolia_docs.py for proper parsing,
code-fence handling, priority ranking, and atomic replacement.
"""

import sys
import subprocess
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parents[1]
    sync_script = repo_root / ".github" / "scripts" / "sync_algolia_docs.py"
    cmd = [sys.executable, str(sync_script)] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
