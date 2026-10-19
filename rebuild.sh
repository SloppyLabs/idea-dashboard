#!/usr/bin/env bash
# Rebuild the idea-dashboard with the community-flags API endpoint.
set -euo pipefail
cd "$(dirname "$0")"
export FLAGS_API="${FLAGS_API:-https://idea-dashboard.ooixinsheng.workers.dev}"
exec python3 build.py
