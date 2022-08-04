import os
import argparse
import pathlib
import re
import collections
from glob import glob


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


if __name__ == '__main__':
    opts = get_args()
    folder = os.path.abspath(opts.folder)
    list_file = get_files(folder)
    if list_file is not None:
        if opts.start is not None:
            shift = opts.start - 1
            list_file = collections.deque(list_file)
            list_file.rotate(-shift)
            list_file = list(list_file)
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
