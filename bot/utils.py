import os


def abs_path(file, rel_path):
    dir_path = os.path.dirname(os.path.abspath(file))
    return dir_path + os.altsep + rel_path;
