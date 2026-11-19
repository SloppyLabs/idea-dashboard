#!/bin/sh
# Build wrapper: sets FLAGS_API for the community-flags backend, then runs build.py
cd "$(dirname "$0")"
FLAGS_API="https://idea-dashboard.ooixinsheng.""workers.dev" python3 build.py
