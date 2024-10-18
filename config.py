import os
from pathlib import Path
from typing import Union

BASE_DIR = Path(__file__).parent
DRIVERS_DIR = BASE_DIR / 'drivers'
DUMP_DATA_DIR = BASE_DIR / 'dumps'


def load_paths(path_list: list[Union[str, os.PathLike]]) -> None:
    for path in path_list:
        if not os.path.exists(path):
            os.makedirs(path)
