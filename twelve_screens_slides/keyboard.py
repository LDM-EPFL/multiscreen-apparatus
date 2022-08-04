import os
import subprocess
from pynput.keyboard import Key, Listener
import time

# define the ip
ips = []
pre = '192.168.0'
n = 2
for i in range(n):
    ips.append(f'{pre}.{str(200+i+1)}')
print(ips)

# turn on keyboard listening

def on_press(key):
    try:
        if key.char == 'q':
            for ip in ips:
                # os.system(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff51')
                process = subprocess.Popen(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0x0051'.split(), shell=False)
    except AttributeError:
        if key == Key.backspace:
            # Stop listener
            print('stop streaming keyboard')
            return False
        if key == Key.right:
            for ip in ips:
                # os.system(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff53')
                process = subprocess.Popen(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff53'.split(), shell=False)
        if key == Key.left:
            for ip in ips:
                # os.system(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff51')
                process = subprocess.Popen(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff51'.split(), shell=False)
        if key == Key.page_up:
            for ip in ips:
                # os.system(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff53')
                process = subprocess.Popen(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff51'.split(), shell=False)
        if key == Key.page_down:
            for ip in ips:
                # os.system(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff51')
                process = subprocess.Popen(f'ssh pi@{ip} DISPLAY=:0.0 xdotool key 0xff53'.split(), shell=False)
    time.sleep(1)

def on_release(key):
    if key == Key.backspace:
        # Stop listener
        print('stop streaming keyboard')
        return False

# start listening to keyboard
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
