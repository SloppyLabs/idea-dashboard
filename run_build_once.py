#!/usr/bin/env python3
"""One-shot dashboard build wrapper (avoids inline URL in shell command)."""
import os
import sys

os.environ["FLAGS_API"] = "https://idea-dashboard.ooixinsheng.workers.dev"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import build  # noqa: E402  (import, then invoke)

build.build()

sys.exit(0)
