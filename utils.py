import os


def get_file_name(file_path):
    ''' returns the name of the file in a given path '''
    return os.path.basename(file_path)
