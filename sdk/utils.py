import os
import numpy as np
from datetime import datetime


class StorageTools:
    directory = None
    file_name = None
    file_path = None
    file = None

    def set_directory(self, directory):
        self.directory = directory
        self.file_path = os.path.join(self.directory, f'{self.file_name}')

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')


class CSVStreamWriter(StorageTools):
    def __init__(self, directory: str):
        self.directory = directory

    def open_file(self):
        self.file = open(self.file_path, mode='a')

    def close_file(self):
        self.file.close()

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')

    def write(self, chunk, transpose=False):
        if transpose:
            np.savetxt(fname=self.file, X=np.transpose(chunk), delimiter=',')
        else:
            np.savetxt(fname=self.file, X=chunk, delimiter=',')


class NPYWriter(StorageTools):
    def __init__(self, directory: str):
        self.directory = directory

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.npy':
            raise BaseException('Illegal file extension, *.npy required.')

    def write(self, chunk, transpose=False):
        if transpose:
            # np.save(fname=self.file_path,arr=np.transpose(chunk))
            np.save(file=self.file_path, arr=np.transpose(chunk))
        else:
            np.save(file=self.file_path, arr=np.transpose(chunk))
