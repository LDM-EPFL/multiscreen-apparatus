import os
from glob import glob

import os
from glob import glob

cwd = os.getcwd()
folder = "data_folder"
dir = cwd
print(dir)

folders = sorted(glob(f'{folder}/*'))

files = []
for folder in folders:
    files.extend(sorted(glob(f'{folder}/*')))
print(files)

for i in range(6):
    path = os.path.join(dir, f'screen_{i+1}')
    if not os.path.exists(path):
        os.mkdir(path)

for i in range(len(files)):
    file_name = ""
    if i % 6 == 0:
        file_name = "screen_1\\1_{:03d}.jpg".format(i // 6)
    if i % 6 == 1:
        file_name = "screen_2\\2_{:03d}.jpg".format(i // 6)
    if i % 6 == 2:
        file_name = "screen_3\\3_{:03d}.jpg".format(i // 6)
    if i % 6 == 3:
        file_name = "screen_4\\4_{:03d}.jpg".format(i // 6)
    if i % 6 == 4:
        file_name = "screen_5\\5_{:03d}.jpg".format(i // 6)
    if i % 6 == 5:
        file_name = "screen_6\\6_{:03d}.jpg".format(i // 6)
    file = files[i]
    dest = dir + "\{}".format(file_name)
    os.system(f'copy \"{file}\" \"{dest}\"')
    # print(dir + "\{}".format(files[i]) + " renamed to " + dir + "\{}".format(file_name))

