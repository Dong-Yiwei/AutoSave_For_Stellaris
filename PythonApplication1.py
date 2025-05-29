# -*- coding: gbk -*-
import os
import time
import shutil
from datetime import datetime

# ��ʼ������
WATCH_FOLDER = r'C:\Users\34355\Documents\Paradox Interactive\Stellaris\save games'  # Ŀ����ļ���
CHECK_INTERVAL = 2  # �����
seconds=3 # �ж����£�s��
N=input(f'��������Ҫ�Ĵ浵������������ֵΪ20 ��')
n=N # ��󱣴������������ʱ��ɾ��ǰN/2��Ȼ���������
# ===========================
file_timestamps = {} # ���ڼ�¼���µı༭ʱ��
file_save = {} # ���ڼ�¼�Ѵ���ļ�
start_time = time.time()  # ��������ʱ��

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
    return sorted(files, key=lambda x: x[1])  # ��ʱ������

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
    # �ж�ĳ���ļ�������� seconds �����Ƿ����ļ�����
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
    # ��ȡ WATCH_FOLDER �����ڸ��µ����ļ���
    print(f"�������ļ���")
    while True:
        for name in os.listdir(WATCH_FOLDER):
            full_path = os.path.join(WATCH_FOLDER, name)
            if os.path.isdir(full_path):
                if is_folder_updating(full_path, seconds):
                    print(f"�ɹ��ҵ��ļ��У�{full_path}")
                    return full_path

def monitor_folder(UPDATA_FOLDER,N):
    print(f"��ʼ���ӣ�{UPDATA_FOLDER}")
    while True:
        try:
            Files = [f for f in os.listdir(UPDATA_FOLDER) if is_autosave(f)]
            for filename in Files:
                full_path = os.path.join(UPDATA_FOLDER,filename)

                if N<0:
                    del_old(UPDATA_FOLDER,n)
                    N=refresh_N(n)

                if  os.path.getmtime(full_path) < start_time :
                    continue # �������ڳ�������ǰ���ڵ��ļ�
                    
                last_modified = os.path.getmtime(full_path)
                    
                if filename not in file_timestamps or file_timestamps[filename] < last_modified:
                    file_timestamps[filename] = last_modified
                    handsave_name = generate_handsave_filename(filename)
                    handsave_path = os.path.join(UPDATA_FOLDER, handsave_name)

                    shutil.copy2(full_path, handsave_path)
                    N=N-1
                    print(f"[{datetime.now()}] �������ļ������£�{filename}������Ϊ��{handsave_name}")

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"����{e}")
            time.sleep(CHECK_INTERVAL)
            break

if __name__ == '__main__':
    UPDATA_FOLDER=finder()
    monitor_folder(UPDATA_FOLDER,N)