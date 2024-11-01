import json
import shutil
from pathlib import Path


shutil.rmtree('../html', ignore_errors=True)
# Path('../html/paged').mkdir(parents=True, exist_ok=True)
shutil.copytree('./assets', '../html/assets', dirs_exist_ok=True)
