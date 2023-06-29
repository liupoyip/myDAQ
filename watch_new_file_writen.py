import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import contextlib


class NewFileHandler(FileSystemEventHandler):

    def __init__(self, path_rec_csv, setting_ver):
        self.path_rec_csv = path_rec_csv
        self.setting_ver = setting_ver

    # TODO:追加新功能在「on_created」
    def on_created(self, event):
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            create_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y%m%dT%H%M%S")
            with open(self.path_rec_csv, 'a') as file:
                with contextlib.redirect_stdout(file):
                    print(f'{create_time},{file_path},{self.setting_ver}')

            print(f'[*] {datetime.now()} New file created: {file_path}')
    


if __name__ == '__main__':
    
    path_target_folder = './monitored_folder'
    path_recording_csv = 'record.csv'
    setting_file = 'setting_file.json'

    path_target_folder = os.path.abspath(path_target_folder)
    path_recording_csv = os.path.abspath(path_recording_csv)
    if not os.path.exists(path_recording_csv):
        open(path_recording_csv, 'a').close()
    print('[+] Start monitoring')
    print(f'   [-] Monitor folder: {path_target_folder}')
    print(f'   [-] Record csv file: {path_recording_csv}')

    event_handler = NewFileHandler(path_recording_csv,setting_ver='setting_file.json')
    observer = Observer()
    observer.schedule(event_handler, path_target_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print('Monitor STOP')