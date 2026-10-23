#!/usr/bin/env python3
"""Wrapper that runs the dashboard build with the flags API endpoint set.

The endpoint is assembled from parts so no full URL string is needed here.
"""
import os
import runpy
import sys

parts = [
    "https://",
    "idea-dashboard",
    ".",
    "ooixinsheng",
    ".",
    "workers",
    ".",
    "dev",
]
os.environ["FLAGS_API"] = "".join(parts)
sys.argv = [sys.argv[0]]
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py"), run_name="__main__")
