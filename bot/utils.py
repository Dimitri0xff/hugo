import os


def abs_path(file, rel_path):
    dir_path = os.path.dirname(os.path.abspath(file))
    return os.path.join(dir_path, rel_path);
