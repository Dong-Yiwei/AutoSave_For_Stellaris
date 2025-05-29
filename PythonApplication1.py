# -*- coding: gbk -*-
import os
import time
import shutil
from datetime import datetime

# 初始化设置
WATCH_FOLDER = r'C:\Users\34355\Documents\Paradox Interactive\Stellaris\save games'  # 目标根文件夹
CHECK_INTERVAL = 2  # 检查间隔
seconds=3 # 判定更新（s）
N=input(f'请输入想要的存档上限数，建议值为20 ：')
n=N # 最大保存数，到达最大时，删掉前N/2，然后继续保存
# ===========================
file_timestamps = {} # 用于记录最新的编辑时间
file_save = {} # 用于记录已存的文件
start_time = time.time()  # 程序启动时间

def is_autosave(filename):
    return filename.lower().startswith('autosave') and filename.endswith('.sav')

def generate_handsave_filename(original):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    original=original.replace('autosave','handsave')
    return f'{original}_{now}.sav'

def get_autosave_files(UPDATA_FOLDER):
    files = []
    for f in os.listdir(UPDATA_FOLDER):
        if f.startswith("handsave") and f.endswith(".sav"):
            full_path = os.path.join(UPDATA_FOLDER, f)
            files.append((full_path, os.path.getmtime(full_path)))
    return sorted(files, key=lambda x: x[1])  # 按时间升序

def refresh_N(n):
    n=(n-int(n/2))
    return n

def del_old(UPDATA_FOLDER,n):
    files = get_autosave_files(UPDATA_FOLDER)
    for file_path, _ in files[:int(n/2)]:
        try:
            os.remove(file_path)
            print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Failed to delete")

def is_folder_updating(folder_path,seconds):
    # 判断某个文件夹在最近 seconds 秒内是否有文件更新
    now = time.time()
    for root, _, files in os.walk(folder_path):
        for f in files:
            file_path = os.path.join(root, f)
            try:
                if os.path.getmtime(file_path) > now - seconds:
                    return True
            except Exception:
                continue
    return False

def finder():
    # 获取 WATCH_FOLDER 下正在更新的子文件夹
    print(f"正在找文件夹")
    while True:
        for name in os.listdir(WATCH_FOLDER):
            full_path = os.path.join(WATCH_FOLDER, name)
            if os.path.isdir(full_path):
                if is_folder_updating(full_path, seconds):
                    print(f"成功找到文件夹，{full_path}")
                    return full_path

def monitor_folder(UPDATA_FOLDER,N):
    print(f"开始监视：{UPDATA_FOLDER}")
    while True:
        try:
            Files = [f for f in os.listdir(UPDATA_FOLDER) if is_autosave(f)]
            for filename in Files:
                full_path = os.path.join(UPDATA_FOLDER,filename)

                if N<0:
                    del_old(UPDATA_FOLDER,n)
                    N=refresh_N(n)

                if  os.path.getmtime(full_path) < start_time :
                    continue # 跳过早于程序允许前存在的文件
                    
                last_modified = os.path.getmtime(full_path)
                    
                if filename not in file_timestamps or file_timestamps[filename] < last_modified:
                    file_timestamps[filename] = last_modified
                    handsave_name = generate_handsave_filename(filename)
                    handsave_path = os.path.join(UPDATA_FOLDER, handsave_name)

                    shutil.copy2(full_path, handsave_path)
                    N=N-1
                    print(f"[{datetime.now()}] 发现新文件并更新：{filename}，保存为：{handsave_name}")

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"出错：{e}")
            time.sleep(CHECK_INTERVAL)
            break

if __name__ == '__main__':
    UPDATA_FOLDER=finder()
    monitor_folder(UPDATA_FOLDER,N)