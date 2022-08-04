import socket
import os
import time
import art
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='process a folder into m3u')
    parser.add_argument('--nowait', action='store_true')
    return parser.parse_args()

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

if __name__ == '__main__':

    os.system('clear')

    opts = get_args()

    if not opts.nowait:
        time.sleep(15)

    ip_name = str(extract_ip())
    size = os.get_terminal_size()
    padding_h  = int((size.columns - len(ip_name))/2)
    padding_v =  int((size.lines - 4)/2)
    # for i in range(padding_v):
    #     print(" ")
    # print(size.columns * "-")
    # print((padding_h * " ") + ip_name)
    # print(size.columns * "-")
    # for i in range(padding_v):
    #     print(" ")

    with open("GANGBUK/mxdlogo.txt", 'r') as f:
        print(f.read())

    art.tprint("CIRCULAR GANGBUK", font="univers")
    art.tprint(ip_name, font="univers")
