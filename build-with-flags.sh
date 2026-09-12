#!/bin/bash
# Wrapper: sets FLAGS_API for the dashboard build (community flags backend on Workers)
export FLAGS_API="https://idea-dashboard.ooixinsheng.workers.dev"
cd "$(dirname "$0")" || exit 1
exec python3 build.py
