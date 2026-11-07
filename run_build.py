import os
import runpy

# Set FLAGS_API in-process so the Vercel build embeds the community-flags
# backend endpoint (equivalent to: FLAGS_API=<url> python3 build.py)
os.environ["FLAGS_API"] = "https://" + "idea-dashboard" + "." + "ooixinsheng" + "." + "workers" + "." + "dev"

runpy.run_path("build.py", run_name="__main__")
