import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileSystemEvent

import mysql.connector
import mysql.connector.cursor
from typing import Optional


class MySQLDataUploader(FileSystemEventHandler):


    db = None
    cursor:Optional[mysql.connector.cursor.MySQLCursor] = None
    host = None
    port = None
    user = None
    password = None
    db_name = None
    rawdata_table_name = None
    headers = None
    data_types = None
    values = None
    cfg_path = None
    cfg = None
    current_data:tuple = None
    rawdata_table_name = None


    def __init__(self,target_dir,cfg_path):
        self.target_dir = target_dir
        self.cfg_path = cfg_path
        self.read_cfg()
    

    def read_cfg(self):
        with open(self.cfg_path) as file:
            cfg = json.load(file)

        self.host = cfg['host']
        self.port = cfg['port']
        self.user = cfg['user']
        self.password = cfg['password']
        self.db_name = cfg['machine']
        self.rawdata_table_name = cfg['rawdata_table_name']
        self.headers = cfg['headers']
        self.data_types = cfg['data_types']
        self.values = cfg['values']
        self.rawdata_table_name = cfg['rawdata_table_name']
        

    def set_current_data(self,current_data):
        # TODO: 之要串正確的data
        self.current_data = current_data


    def connect_to_server(self):
        print('connect to mysql server...', end='')
        self.db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password)
        print('Done!')
        
    
    def use_database(self):
        sql = f'USE {self.db_name}'
        print(f'execute sql command: {sql}')
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
    

    def create_database(self):
        sql = f'CREATE DATABASE IF NOT EXISTS {self.db_name}'
        print(f'execute sql command: {sql}')
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        

    def create_rawdata_table(self):
        sql = f'CREATE TABLE IF NOT EXISTS {self.rawdata_table_name} ('
        for header,data_type in zip(self.headers,self.data_types):
            sql = f'{sql}{header} '
            sql = f'{sql}{data_type}, '
        sql = sql[:-2]
        sql = f'{sql})'

        print(f'execute sql command: {sql}')
        self.cursor.execute(sql)
    

    def append_rawdata(self):
        sql = f'INSERT INTO {self.rawdata_table_name} ('
        for header in self.headers:
            sql = f'{sql}{header}, '
        sql = sql[:-2]
        sql = f'{sql}) '
        sql = f'{sql}VALUES ('
        for value in self.values:
            sql = f'{sql}{value}, '
        sql = sql[:-2]
        sql = f'{sql})'
        
        print(f'execute sql command: {sql}')
        print(f'insert value: {self.current_data}')
        self.cursor.execute(sql,self.current_data)
        self.db.commit()


    def on_created(self, event:FileSystemEvent):
        if event.is_directory:
            
            # TODO: 找到新增的資料夾
            print(f'new directory created: {event.src_path}')
            print(f'uploading file to database...',end='')
            self.create_database()
            self.use_database()
            self.create_rawdata_table()

            timestamp = os.path.basename(event.src_path)
            dummy_data = ('task',timestamp,os.path.join(event.src_path,'cfg.json'))
            self.set_current_data(dummy_data)
            self.append_rawdata()
            print(f'Done!!')
    

# TODO: 之後要把task and export path從 ./models/record_cfg.json 撈出來

uploader_cfg_path = 'cfg.json'
with open(uploader_cfg_path,'r') as file:
    cfg = json.load(file)


task_name = cfg['task']
database_dir = cfg['database_dir']
lab=cfg['lab']

machine = cfg['machine']
table_name = cfg['rawdata_table_name']
target_dir = os.path.join(task_name,database_dir,lab,machine,table_name,task_name)
print(f'target directory: {target_dir}')

uploader = MySQLDataUploader(target_dir=target_dir,cfg_path=uploader_cfg_path)
print('--- Start monitoring ---')
print(f'Monitor folder: {target_dir}')

uploader.connect_to_server()
observer = Observer()
observer.schedule(uploader, target_dir, recursive=False)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
print('Monitor STOP')