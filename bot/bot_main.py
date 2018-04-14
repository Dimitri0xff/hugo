import os
import logging

from bot import utils
from .config import load_commands_folder

TOKEN_FILE_REL_PATH = '../token.txt'
CONFIG_FOLDER_PATH = 'config/bot/'
COMMAND_START_CHAR = '!'

_client = None
_all_commands = []
_name_to_command = {}


def run(client, args):
    global _client
    _client = client
    token = _init()
    _reload()
    client.run(token)


def _init():
    logging.basicConfig(level=logging.INFO)

    return _load_token()


def _load_token():
    file_path = utils.abs_path(__file__, TOKEN_FILE_REL_PATH)
    key_file = open(file_path)
    return key_file.read()


def _reload():
    global _all_commands
    folder_path = CONFIG_FOLDER_PATH
    _all_commands = []
    _all_commands.extend(load_commands_folder(folder_path))

    for command in _all_commands:
        for name in command.names:
            _name_to_command[name] = command


async def on_message(message):
    if not message.content.startswith(COMMAND_START_CHAR):
        return
    keyword, *args = message.content.split(' ', maxsplit=1)
    keyword = keyword[1:]

    command = _name_to_command.get(keyword)
    if command:
        await command.message(_client, message, keyword, args)
