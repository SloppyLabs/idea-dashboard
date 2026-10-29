#!/bin/bash
# One-shot dashboard rebuild with community-flags backend env var
cd "$(dirname "$0")"
export FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev"
exec python3 build.py
