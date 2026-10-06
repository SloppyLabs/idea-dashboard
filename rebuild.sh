#!/bin/bash
# Rebuild the idea dashboard with the flags API endpoint baked in.
set -e
cd "$(dirname "$0")"
export FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev"
exec python3 build.py
