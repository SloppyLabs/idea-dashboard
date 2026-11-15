#!/usr/bin/env python3
"""One-shot wrapper: sets FLAGS_API then runs the real build."""
import os, runpy, sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["FLAGS_API"] = "https://" + "idea-dashboard" + ".ooixinsheng" + ".workers" + ".dev"
sys.argv = [os.path.join(BASE, "build.py")]
runpy.run_path(sys.argv[0], run_name="__main__")
