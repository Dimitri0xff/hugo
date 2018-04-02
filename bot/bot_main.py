import os
import logging
from .config import load_commands_folder

TOKEN_FILE_PATH = 'token.txt'
CONFIG_FOLDER_PATH = 'config/bot/'
COMMAND_START_CHAR = '!'

_client = None
_token = None
_all_commands = []
_name_to_command = {}


def run(client, args):
    global _client
    _client = client
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
        response = command.message(command, keyword, args)
        if response:
            await _client.send_message(message.channel, response) # FIXME: probably need Ioc and DI here
