#!/bin/bash
# One-shot dashboard rebuild wrapper (avoids inline URL in shell history).
cd "$(dirname "$0")"
FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev" python3 build.py
