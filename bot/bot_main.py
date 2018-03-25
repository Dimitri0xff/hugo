import os
import logging
from .config import load_commands_folder

TOKEN_FILE_PATH = 'token.txt'
CONFIG_FOLDER_PATH = 'config/bot/'

_token = None
_all_commands = []

def run(client, args):
    #
    _init()
    _reload()
    client.run(_token)


def _init():
    global _token
    logging.basicConfig(level=logging.INFO)

    key_file = open(TOKEN_FILE_PATH)
    _token = key_file.read()
    key_file.close()


def _reload():
    global _all_commands
    folder_path = CONFIG_FOLDER_PATH
    _all_commands = []
    _all_commands.extend(load_commands_folder(folder_path))

