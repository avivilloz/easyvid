import os
import glob


def list_subpaths(dir_path):
    return glob.glob(os.path.join(dir_path, "*"))


def list_file_paths(dir_path):
    return [f for f in list_subpaths(dir_path=dir_path) if os.path.isfile(f)]
