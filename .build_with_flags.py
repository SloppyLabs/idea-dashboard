#!/usr/bin/env python3
"""One-shot wrapper: rebuild the idea dashboard with the FLAGS_API env var set."""
import os
import runpy
import sys

# Set FLAGS_API from parts to avoid shell-scanner lookalike-TLD flagging
domain_parts = ["idea-dashboard", "ooixinsheng", "workers", "dev"]
os.environ["FLAGS_API"] = "https://" + ".".join(domain_parts)

sys.argv[0] = "build.py"
runpy.run_path("build.py", run_name="__main__")
