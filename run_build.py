#!/usr/bin/env python3
"""One-shot wrapper: runs build.py with the FLAGS_API env var set for Vercel community flags."""
import os
import runpy
import sys

os.environ["FLAGS_API"] = "https://idea-dashboard.ooixinsheng.workers.dev"

# Execute build.py in this directory with the env var applied
sys.argv = ["build.py"]
runpy.run_path("build.py", run_name="__main__")
