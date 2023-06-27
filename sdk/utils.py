import os
import sys
import numpy as np
import inspect
from datetime import datetime
from debug_flags import PRINT_FUNC_NAME_FLAG


class StorageTools:

    def __init__(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        self.directory = None
        self.file_name = None
        self.file_path = None
        self.file = None
        self.writer_type = None

    def set_directory(self, directory):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_directory)}')

        self.directory = directory

    def set_file_name(self, file_name):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_file_name)}')

        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)


class CSVStreamWriter(StorageTools):

    def __init__(self, directory: str):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super(StorageTools, self).__init__()
        self.writer_type = 'stream'
        self.directory = directory

    def check_file_extension(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.check_file_extension)}')

        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')

    def open_file(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.open_file)}')

        self.file = open(self.file_path, mode='a')

    def close_file(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.close_file)}')

        if self.file != None:
            self.file.close()

    def write(self, chunk, transpose=False):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.write)}')

        if transpose:
            np.savetxt(fname=self.file, X=np.transpose(chunk), delimiter=',')
        else:
            np.savetxt(fname=self.file, X=chunk, delimiter=',')


class NPYWriter(StorageTools):

    def __init__(self, directory: str):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super(NPYWriter, self).__init__()
        self.directory = directory
        self.writer_type = 'segment'
        self.write_file_count = 0

    def reset_write_file_count(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.reset_write_file_count)}')

        self.write_file_count = 0

    def check_file_extension(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.check_file_extension)}')

        name, extension = os.path.splitext(self.file_name)
        if extension != '.npy':
            raise BaseException('Illegal file extension, *.npy required.')

    def write(self, chunk, transpose=False):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.write)}')

        file_path = os.path.join(self.directory, f'{self.write_file_count}.npy')
        if transpose:
            np.save(file=file_path, arr=np.transpose(chunk))
        else:
            np.save(file=file_path, arr=np.transpose(chunk))
        self.write_file_count += 1


def get_func_name(func):
    func_name = inspect.getmembers(func, inspect.isfunction)[0][1]
    return f'{func_name}'
