import os
import time
import random
import subprocess
from glob import glob

file = glob('LDM/slide/*.odp')[-1]

k = f"soffice --norestore --invisible --show {file}"

subprocess.Popen(k.split(), env=dict(os.environ, DISPLAY=":0.0"), shell=False)
