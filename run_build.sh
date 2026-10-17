#!/bin/bash
# Rebuild the idea dashboard with the community-flags API endpoint configured.
export FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev"
cd "$(dirname "$0")"
exec python3 build.py
