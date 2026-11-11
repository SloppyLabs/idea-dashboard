#!/usr/bin/env python3
"""One-shot dashboard build wrapper: runs build.py with the FLAGS_API env var
set to the Cloudflare Worker backend (community flags)."""
import os
import subprocess
import sys

os.environ["FLAGS_API"] = "https://idea-dashboard.ooixinsheng.workers.dev"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
result = subprocess.run(
    [sys.executable, "build.py"],
    env=os.environ,
)
sys.exit(result.returncode)
