import collections
from unittest import mock

import discord

from bot import bot_main
from test.async_test_utils import AsyncMock, run_coro
from test.test_case_base import TestCaseBase

MockMessage = collections.namedtuple('MockMessage', 'channel content')


def create_message(channel, msg):
    message = MockMessage(channel=channel, content=msg)
    return message


class BasicCommandTest(TestCaseBase):

    def __init__(self, *argc, **argv):
        super(BasicCommandTest, self).__init__(*argc, **argv)
        self.mock_client = None

    def run_command(self, msg_text, expected_text):
        from discord.client import Client
        self.mock_client.send_message = Client.send_message
        msg1 = create_message(12, msg_text)

        run_coro(bot_main.on_message(msg1))

        Client.send_message.mock.assert_called_once_with(12, expected_text)
        Client.send_message.mock.reset_mock()

    @mock.patch('bot.bot_main._load_token')
    def setUp(self, mock_load_token):

        bot_main.CONFIG_FOLDER_PATH = self.abs_path(__file__, 'config')
        self.mock_client = mock.create_autospec(discord.Client)
        args = {}
        mock_load_token.return_value = 'test_token'

        bot_main.run(self.mock_client, args)

        self.mock_client.run.assert_called_with('test_token')

    @mock.patch('discord.client.Client.send_message', new=AsyncMock())
    def test_simple_commands(self):
        self.run_command('!cmd1name1', 'Cmd1 text')
        self.run_command('!cmd1name2', 'Cmd1 text')
        self.run_command('!cmd1name3', 'Cmd1 text')
        self.run_command('!cmd1name4', 'Cmd1 text')
        self.run_command('!cmd2name1', 'Cmd2 text')
        self.run_command('!cmd91name1', 'Cmd91 text')

    @mock.patch('discord.client.Client.send_message', new=AsyncMock())
    def test_multiline_commands(self):
        self.run_command('!cmd3name1', 'Cmd3 line1\nCmd3 line2\nCmd3 line3\nCmd3 line4\nCmd3 line5')
        self.run_command('!cmd3name2', 'Cmd3 line1\nCmd3 line2\nCmd3 line3\nCmd3 line5')
        self.run_command('!cmd3name3', 'Cmd3 line1\nCmd3 line4')

        self.run_command('!cmd4name1', '') # TODO: re-think this config/behavior
        self.run_command('!cmd4name2', 'Cmd4 line1')
