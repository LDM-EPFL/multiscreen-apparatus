import os
from glob import glob

cwd = os.getcwd()
folder = "data_folder"
dir = cwd
print(dir)

folders = sorted(glob(f'{folder}/*'))

for i in range(6):
    path = os.path.join(dir, f'screen_{i+1}')
    if not os.path.exists(path):
        os.mkdir(path)

files = []
folder_num = 0
for folder in folders:
    files = sorted(glob(f'{folder}/*'))
    screen_count = 0
    for file in files:
        filename = os.path.basename(file)
        file_, ext = os.path.splitext(filename)
        print(filename)
        screen_num = screen_count % 6 + 1
        image_num = screen_count // 6
        file_name = f'screen_{screen_num}\\{folder_num}_{image_num}{ext}'
        dest = dir + "\\{}".format(file_name)
        print(dest)
        os.system(f'copy \"{file}\" \"{dest}\"')
        screen_count += 1
    folder_num += 1
