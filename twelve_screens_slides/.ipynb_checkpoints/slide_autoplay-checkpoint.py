import os
import time
import random

# positioning the slides:
breakdown = str(random.randrange(1,13))
for ky in breakdown:
    os.system(f'DISPLAY=:0.0 xdotool key {ky}')
os.system('DISPLAY=:0.0 xdotool key 0xff0d') 
        
time.sleep(random.randrange(20,30))

while True:
    os.system("DISPLAY=:0.0 xdotool key 0xff53")
    time.sleep(random.randrange(20,30))
