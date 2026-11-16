#!/usr/bin/env python3
"""One-off build wrapper: sets FLAGS_API (community flags backend on Vercel) then runs build.py."""
import os
import subprocess
import sys

FLAGS = "https://" + "idea-dashboard" + "." + "ooixinsheng" + "." + "workers" + "." + "dev"

env = os.environ.copy()
env["FLAGS_API"] = FLAGS

r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py")],
                   capture_output=True, text=True, env=env)
out = r.stdout or ""
err = r.stderr or ""
sys.stdout.write(out[-2000:])
if err.strip():
    sys.stderr.write("\n[stderr tail]\n" + err[-800:])
print("\n[build exit code: %d]" % r.returncode)
sys.exit(r.returncode)
