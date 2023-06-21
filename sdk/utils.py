import os
import numpy as np
from datetime import datetime


class StorageTools:

    def __init__(self) -> None:
        self.directory = None
        self.file_name = None
        self.file_path = None
        self.file = None
        self.writer_type = None

    def set_directory(self, directory):
        self.directory = directory

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)


class CSVStreamWriter(StorageTools):

    def __init__(self, directory: str):
        super(StorageTools, self).__init__()
        self.writer_type = 'stream'
        self.directory = directory

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')

    def open_file(self):
        self.file = open(self.file_path, mode='a')

    def close_file(self):
        if self.file != None:
            self.file.close()

    def write(self, chunk, transpose=False):
        if transpose:
            np.savetxt(fname=self.file, X=np.transpose(chunk), delimiter=',')
        else:
            np.savetxt(fname=self.file, X=chunk, delimiter=',')


class NPYWriter(StorageTools):

    def __init__(self, directory: str):
        super(NPYWriter, self).__init__()
        self.directory = directory
        self.writer_type = 'segment'
        self.write_file_count = 0

    def reset_write_file_count(self):
        self.write_file_count = 0

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.npy':
            raise BaseException('Illegal file extension, *.npy required.')

    def write(self, chunk, transpose=False):
        file_path = os.path.join(self.directory, f'{self.write_file_count}.npy')
        if transpose:
            np.save(file=file_path, arr=np.transpose(chunk))
        else:
            np.save(file=file_path, arr=np.transpose(chunk))
        self.write_file_count += 1
