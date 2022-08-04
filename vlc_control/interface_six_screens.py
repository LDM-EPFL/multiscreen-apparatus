import requests
from requests.auth import HTTPBasicAuth
from pynput.keyboard import Key, Listener
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import time
from xml.dom import minidom

import asyncio
import aiohttp
from aiohttp import ClientSession


# ports = ['8080', '8081', '8082', '8083']
ports = ['8080', '8081', '8082', '8083', '8084', '8085' ]
#ports = ['8080']
# ip = "localhost"
# ips = ["128.179.183.74", "128.179.164.252", "128.179.162.243"]
# ips = ["128.179.178.218", "128.179.167.103", "128.179.163.65"]
# ips = ["128.179.182.217", "128.179.162.29", "128.179.167.89"]
ips = ["localhost"]
url = "/requests/status.xml"
password = '12345'

commands = dict()
commands['start'] = "?command=pl_play&id=0"
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

ip_ports = []

'''for ip in ips:
    for port in ports:
        urls.append([ip, port])'''

for port in ports:
    for ip in ips:
        ip_ports.append([ip, port])

ready = False

if not ready:
    val = input("Are you ready? (y/n) : ")

    if val == 'y' or val == 'Y':
        ready = True


'''
def control(command):
    vlc_requests = []
    for url in urls:
        vlc_requests.append([url, command])
    with PoolExecutor(max_workers=12) as executor:
        for _ in executor.map(con_control, vlc_requests):
            pass'''


async def fetch(_url, session):
    async with session.get(_url) as response:
        return await response.read()


def control(command, args):
    commands, ip_ports, url, password = args[0], args[1], args[2], args[3]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_control(command, commands, ip_ports, url, password))
    if command == 'start' or command == 'next' or command == 'previous':
        loop0 = asyncio.new_event_loop()
        loop0.run_until_complete(async_control('vol_to_zero', commands, ip_ports, url, password))
        time.sleep(0.5)
        loop1 = asyncio.new_event_loop()
        loop1.run_until_complete(async_control('seek_to_zero', commands, ip_ports, url, password))
        loop2 = asyncio.new_event_loop()
        loop2.run_until_complete(async_control('pause', commands, ip_ports, url, password))
        loop3 = asyncio.new_event_loop()
        loop3.run_until_complete(async_control('vol_to_full', commands, ip_ports, url, password))


async def async_control(command, commands, ip_ports, url, password):
    tasks = []
    auth = aiohttp.BasicAuth(login='', password=password)
    async with ClientSession(auth=auth) as session:
        for ip_port in ip_ports:
            req = commands[command]
            ip = ip_port[0]
            port = ip_port[1]
            _url = "http://" + ip + ":" + port + url + req
            task = asyncio.ensure_future(fetch(_url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses


def seek_to_start(args):
    commands, ip_ports, url, password = args[0], args[1], args[2], args[3]
    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_seek_to_start(ip_ports, url, password))


async def async_seek_to_start(ip_ports, url, password):
    req = "?command=seek&val=0"
    tasks = []
    auth = aiohttp.BasicAuth(login='', password=password)
    async with ClientSession(auth=auth) as session:
        for ip_port in ip_ports:
            ip = ip_port[0]
            port = ip_port[1]
            _url = "http://" + ip + ":" + port + url + req
            task = asyncio.ensure_future(fetch(_url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses


def pause_play(ip_ports):
    with PoolExecutor(max_workers=8) as executor:
        for _ in executor.map(con_pause_play, ip_ports):
            pass


def con_pause_play(url_req):
    ip = url_req[0]
    port = url_req[1]
    xml = None
    try:
        xml = requests.get("http://" + ip + ":" + port + url, auth=HTTPBasicAuth('', password))
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))
    if xml:
        respond = minidom.parseString(xml.content)
        state = respond.getElementsByTagName('state')
        status = state[0].firstChild.data
        if status == 'paused':
            try:
                xml = requests.get("http://" + ip + ":" + port + url + commands['pause'], auth=HTTPBasicAuth('', password))
            except requests.exceptions.HTTPError as errh:
                print("An Http Error occurred:" + repr(errh))
            except requests.exceptions.ConnectionError as errc:
                print("An Error Connecting to the API occurred:" + repr(errc))
            except requests.exceptions.Timeout as errt:
                print("A Timeout Error occurred:" + repr(errt))
            except requests.exceptions.RequestException as err:
                print("An Unknown Error occurred" + repr(err))
        if status == 'playing':
            try:
                xml = requests.get("http://" + ip + ":" + port + url + commands['pause'], auth=HTTPBasicAuth('', password))
            except requests.exceptions.HTTPError as errh:
                print("An Http Error occurred:" + repr(errh))
            except requests.exceptions.ConnectionError as errc:
                print("An Error Connecting to the API occurred:" + repr(errc))
            except requests.exceptions.Timeout as errt:
                print("A Timeout Error occurred:" + repr(errt))
            except requests.exceptions.RequestException as err:
                print("An Unknown Error occurred" + repr(err))

def on_press(key):
    args = [commands, ip_ports, url, password]
    args_1 = [commands, [ip_ports[0]], url, password]
    args_2 = [commands, [ip_ports[1]], url, password]
    args_3 = [commands, [ip_ports[2]], url, password]
    args_4 = [commands, [ip_ports[3]], url, password]
    args_5 = [commands, [ip_ports[4]], url, password]
    args_6 = [commands, [ip_ports[5]], url, password]
    args_13 = [commands, ip_ports[:3], url, password]
    args_46 = [commands, ip_ports[3:], url, password]
    args_14 = [commands, [ip_ports[0], ip_ports[3]], url, password]
    args_25 = [commands, [ip_ports[1], ip_ports[4]], url, password]
    args_36 = [commands, [ip_ports[2], ip_ports[5]], url, password]
    if ready:
        print('{0} pressed'.format(
            key))
        try:
            if key.char == '1':
                control('start', args)
            if key.char == '2':
                control('stop', args)
            if key.char == '9':
                control('sort', args)
            if key.char == '0':
                control('fullscreen', args)
            if key.char == '.':
                pause_play(ip_ports)
            if key.char == '5':
                seek_to_start(args)
            if key.char == 'q':
                control('previous', args_1)
            if key.char == 'w':
                control('next', args_1)
            if key.char == 'e':
                control('previous', args_2)
            if key.char == 'r':
                control('next', args_2)
            if key.char == 't':
                control('previous', args_3)
            if key.char == 'y':
                control('next', args_3)
            if key.char == 'a':
                control('previous', args_4)
            if key.char == 's':
                control('next', args_4)
            if key.char == 'd':
                control('previous', args_5)
            if key.char == 'f':
                control('next', args_5)
            if key.char == 'g':
                control('previous', args_6)
            if key.char == 'h':
                control('next', args_6)
            if key.char == 'u':
                control('previous', args_13)
            if key.char == 'i':
                control('next', args_13)
            if key.char == 'j':
                control('previous', args_46)
            if key.char == 'k':
                control('next', args_46)
            if key.char == 'z':
                control('previous', args_14)
            if key.char == 'x':
                control('next', args_14)
            if key.char == 'c':
                control('previous', args_25)
            if key.char == 'v':
                control('next', args_25)
            if key.char == 'b':
                control('previous', args_36)
            if key.char == 'n':
                control('next', args_36)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
            if key == Key.right:
                control('next', args)
            if key == Key.left:
                control('previous', args)
            if key == Key.page_down:
                control('next', args)
            if key == Key.page_up:
                control('previous', args)
            if key == Key.space:
                control('play', args)
            if key == Key.shift:
                control('pause', args)

def on_release(key):
    # print('{0} release'.format(
    #     key))
    if key == Key.backspace:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


def con_control(vlc_request):
    req = commands[vlc_request[1]]
    ip = vlc_request[0][0]
    port = vlc_request[0][1]
    try:
        requests.head("http://" + ip + ":" + port + url + req, auth=HTTPBasicAuth('', password))
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))






