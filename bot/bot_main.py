import os
import logging
import config

TOKEN_FILE_PATH = 'token.txt'
CONFIG_FOLDER_PATH = 'config/bot/'

_token = None


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
    folder_path = CONFIG_FOLDER_PATH
    for name in os.listdir(folder_path):
        path = os.join(folder_path, name)
        if not os.isfile(path):
            continue
        if name.endswith('.xml'):
            config.load_commands(path)
