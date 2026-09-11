import os
import subprocess
import sys

os.environ["FLAGS_API"] = "https://idea-dashboard.ooixinsheng.workers.dev"
sys.exit(subprocess.call([sys.executable, "build.py"]))
