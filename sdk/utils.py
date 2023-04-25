import os
import numpy as np
from datetime import datetime


class CSVStreamWriter:
    def __init__(self, directory: str):
        self.directory = directory
        self.file_name = None
        self.file_path = None
        self.file = None

    def set_directory(self, directory):
        self.directory = directory
        self.file_path = os.path.join(self.directory, f'{self.file_name}')

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)

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
