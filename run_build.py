import os
import runpy
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["FLAGS_API"] = "https://idea-dashboard.ooixinsheng.workers.dev"
sys.argv = ["build.py"]
runpy.run_path("build.py", run_name="__main__")
