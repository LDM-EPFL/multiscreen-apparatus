import socket
import os
import time
import argparse

import os
import argparse
import pathlib
import re
import collections
from glob import glob

import requests
from requests.auth import HTTPBasicAuth
from xml.dom import minidom

import concurrent.futures
import time
import random
from art import *



def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def get_args():
    parser = argparse.ArgumentParser(description='process a folder into m3u')
    parser.add_argument('folder', type=pathlib.Path)
    parser.add_argument('--start', type=int)
    return parser.parse_args()

def get_files(folder):
    if os.path.isdir(folder):
        files = glob(os.path.join(folder, "*.JPG"))
        files.extend(glob(os.path.join(folder, "*.jpg")))
        files.extend(glob(os.path.join(folder, "*.mp4")))
        files = list(set(files))
        files = natural_sort(files)
        return files

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

commands = dict()
commands['start'] = "?command=pl_play&id=0"
commands['start_r'] = "?command=pl_play&id="
commands['play'] = "?command=pl_play"
commands['pause'] = "?command=pl_pause"
commands['stop'] = "?command=pl_stop"
commands['next'] = "?command=pl_next"
commands['previous'] = "?command=pl_previous"
commands['sort'] = "?command=pl_sort&id=0&val=1"
commands['fullscreen'] = "?command=fullscreen"
commands['seek_to_zero'] = "?command=seek&val=0"
commands['vol_to_zero'] = "?command=volume&val=0"
commands['vol_to_full'] = "?command=volume&val=200"
commands['jump'] = f"?command=pl_play&id="
commands['seek'] = "?command=seek&val="
commands['check_status'] = ""


def control(command, args):
    commands, ip_ports, url, password = args[0], args[1], args[2], args[3]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        req = commands[command]
        _url = "http://" + ip + ":" + port + url + req
        future_to_ip_port = {executor.submit(individual_control, ip_port, url, req, password): ip_port for ip_port in ip_ports}
        response = {}
        for future in concurrent.futures.as_completed(future_to_ip_port):
            ip_port = future_to_ip_port[future]
            try:
                data = future.result()
            except:
                data = None
            response[ip_port] = data
        return response

def individual_control(ip_port, url, req, password):
    ip, port = ip_port[0], ip_port[1]
    vlc_request = "http://" + ip + ":" + port + url + req
    try:
        response =  requests.get(vlc_request, auth=HTTPBasicAuth('', password), timeout=1.0)
    except :
        response = None
    return response

def random_jump(args):
    commands, ip_ports, url, password = args[0], args[1], args[2], args[3]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_ip_port = {executor.submit(individual_jump, ip_port,
        url, commands, password): ip_port for i, ip_port in enumerate(ip_ports)}
        response = {}
        for future in concurrent.futures.as_completed(future_to_ip_port):
            ip_port = future_to_ip_port[future]
            try:
                data = future.result()
            except:
                data = None
            response[ip_port] = data
        return response

def individual_jump(ip_port, url, commands, password):
    ip, port = ip_port[0], ip_port[1]
    vlc_playlist = "http://" + ip + ":" + port + "/requests/playlist.xml"
    vlc_status = "http://" + ip + ":" + port + "/requests/status.xml"
    to_play= []
    try:
        response =  requests.get(vlc_status, auth=HTTPBasicAuth('', password), timeout=1.0)
        status = minidom.parseString(response.text).getElementsByTagName('state')
        if status[0].firstChild.nodeValue == 'stopped':
            time.sleep(random.uniform(20.0, 30.0))
    except:
        return None
    try:
        response =  requests.get(vlc_playlist, auth=HTTPBasicAuth('', password), timeout=1.0)
        playlist = minidom.parseString(response.text).getElementsByTagName('leaf')
        for leaf in playlist:
            if leaf.getAttribute("current") == "":
                to_play.append(leaf.getAttribute("id"))
    except:
        return None

    if len(to_play) > 0:
        pid = random.choice(to_play)
        req = commands["jump"]
        vlc_request = "http://" + ip + ":" + port + url + req + pid
        try:
            response =  requests.get(vlc_request, auth=HTTPBasicAuth('', password), timeout=1.0)
            return response
        except :
            response = None
    else:
        return None

if __name__ == '__main__':

    os.system('clear')


    time.sleep(5)

    ip_name = str(extract_ip())
    size = os.get_terminal_size()
    text_width = 201
    padding_h  = int((size.columns - text_width)/2)
    padding_v =  40

    for i in range(padding_v):
        print(" ")
    # print(size.columns * "-")
    # print((padding_h * " ") + ip_name)
    # print(size.columns * "-")
    # for i in range(padding_v):
    #     print(" ")

    with open("GANGBUK/mxdlogo.txt", 'r') as f:
        k = f.readlines()
    for row in k:
        print(padding_h * " " + row.strip("\n"))

    banner=text2art("CIRCULAR GANGBUK",font='univers')
    rows = banner.split('\n')
    for row in rows:
        print(padding_h * " " + row.strip("\n"))

    banner=text2art(ip_name,font='univers')
    rows = banner.split('\n')
    for row in rows:
        print(padding_h * " " + row.strip("\n"))

    for i in range(35):
        print(" ")

    time.sleep(10)

    # start playing
    folder = sorted(glob("LDM/*"))[0]
    folder = os.path.abspath(folder)
    list_file = get_files(folder)
    if list_file is not None:
        for i in range(200):
            os.system(f'echo " ">/dev/tty1')
        parent_folder = os.path.dirname(folder)
        folder_name = os.path.basename(folder)
        media_m3u = os.path.join(parent_folder, folder_name + '.m3u')
        with open(media_m3u, 'w') as f:
            for file in list_file:
                f.write(file + '\n')
        print("start vlc")
        if os.name == "nt":
            os.system(f'START vlc.exe -q --no-osd -L --no-video-title-show --http-port=8080 --repeat --fullscreen --intf http --one-instance \"{media_m3u}\"')
        elif os.name == "posix":
            os.system(f'cvlc -q --no-osd -L --no-video-title-show --http-port=8080 --repeat --fullscreen --intf http --one-instance \"{media_m3u}\" &')

    # addressing players
    ports = ["8080"]
    url = "/requests/status.xml"
    password = 'mxd'
    ip_ports = []
    ips = ["localhost"]

    for port in ports:
        for ip in ips:
            ip_ports.append((ip, port))
    args = [commands, ip_ports, url, password]

    time.sleep(10)
    start = time.time()
    while True:
        # insert code for detecting stopping player and wait for a good 20-30 seconds
        # time.sleep(random.uniform(5.0, 10.0))
        response = random_jump(args)
        time.sleep(0.5)
        response = control('check_status', args)
        for k in response:
            if k == ('localhost', '8080'):
                if response[k] is None:
                    print("local player is not detected, restart the system")
                    # os.system("sudo reboot")
                else:
                    length = minidom.parseString(response[k].text).getElementsByTagName('length')
                    length = length[0].firstChild.nodeValue
                    information = minidom.parseString(response[k].text).getElementsByTagName('information')
                    category = information[0].getElementsByTagName('category')[0]
                    infos = category.getElementsByTagName("info")
                    for info in infos:
                        if info.getAttribute('name') == "title":
                            title_name = info.firstChild.nodeValue
                    if title_name.split('.')[-1] == "mp4":
                        length = int(length)
                        if length < 15:
                            length = 15
                        time.sleep(length)
                    else:
                        time.sleep(random.uniform(6.0, 10.0))
        if random.random() < 0.005:
            os.system("sudo reboot")
