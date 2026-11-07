#!/bin/bash
# One-shot dashboard rebuild wrapper (avoids inline env-var hostnames in cron shell history)
cd "$(dirname "$0")"
export FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev"
python3 build.py
