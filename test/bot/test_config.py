from operator import attrgetter

from bot import config
from bot.bot_main import CONFIG_FOLDER_PATH
from test.test_case_base import TestCaseBase


class TestConfig(TestCaseBase):

    def test_load_commands_folder(self):
        folder_path = self.abs_path(__file__, '../../' + CONFIG_FOLDER_PATH)
        commands = config.load_commands_folder(folder_path)
        self.assertIsNotNone(commands)
        self.assertTrue(len(commands) > 0)
        for cmd in commands:
            self._check_command_interface(cmd)

    _TEST_COMMANDS_XML_LENGTH = 5

    def test_load_commands_folder_test_config(self):
        folder_path = self.abs_path(__file__, 'config')
        commands = config.load_commands_folder(folder_path)
        self.assertIsNotNone(commands)
        self.assertTrue(len(commands) == self._TEST_COMMANDS_XML_LENGTH)
        commands = sorted(commands, key=attrgetter('desc'))
        for i in range(len(commands)):
            cmd = commands[i]
            self._check_command_interface(cmd)

            # text and name tags/text tags will be tested with on_message to keep the test black box
            # they are not part of the interface
            if i == 0:
                self.assertListEqual(cmd.names, ['cmd1name1', 'cmd1name2', 'cmd1name3', 'cmd1name4'])
                self.assertEqual(cmd.desc, 'Cmd1 desc')
            elif i == 1:
                self.assertListEqual(cmd.names, ['cmd2name1'])
                self.assertEqual(cmd.desc, 'Cmd2 desc')
            elif i == 2:
                self.assertListEqual(cmd.names, ['cmd3name1', 'cmd3name2', 'cmd3name3'])
                self.assertEqual(cmd.desc, 'Cmd3 desc')
            elif i == 3:
                self.assertListEqual(cmd.names, ['cmd4name1', 'cmd4name2'])
                self.assertEqual(cmd.desc, 'Cmd4 desc')
            elif i == 4:
                self.assertListEqual(cmd.names, ['cmd91name1'])
                self.assertEqual(cmd.desc, 'Cmd91 desc')
            else:
                self.fail()

    def _check_command_interface(self, cmd):
        # true: not None, not '' and not []
        # Command duck typing: .names, .desc, .text are mandatory
        self.assertTrue(len(cmd.names) > 0)
        for name in cmd.names:
            self.assertTrue(name)
        self.assertTrue(cmd.desc)
        self.assertTrue(hasattr(cmd, 'message'))
