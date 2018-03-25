from operator import attrgetter

from bot import config
from bot.bot_main import CONFIG_FOLDER_PATH
from bot.error import InvalidConfigurationError
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

            if i == 0:
                self.assertListEqual(cmd.names, ['cmd1name1', 'cmd1name2', 'cmd1name3', 'cmd1name4'])
                self.assertEqual(cmd.desc, 'Cmd1 desc')
                self.assertEqual(cmd.text, 'Cmd1 text')
            elif i == 1:
                self.assertListEqual(cmd.names, ['cmd2name1'])
                self.assertEqual(cmd.desc, 'Cmd2 desc')
                self.assertEqual(cmd.text, 'Cmd2 text')
            elif i == 2:
                self.assertListEqual(cmd.names, ['cmd3name1', 'cmd3name2', 'cmd3name3'])
                self.assertEqual(cmd.desc, 'Cmd3 desc')
                self.assertEqual(cmd.text, 'Cmd3 line1\nCmd3 line2\nCmd3 line3\nCmd3 line4')
                # name tags/text tags will be tested with on_message to keep the test black box
            elif i == 3:
                self.assertListEqual(cmd.names, ['cmd4name1', 'cmd4name2'])
                self.assertEqual(cmd.desc, 'Cmd4 desc')
                self.assertEqual(cmd.text, 'Cmd4 line1')
            elif i == 4:
                self.assertListEqual(cmd.names, ['cmd91name1'])
                self.assertEqual(cmd.desc, 'Cmd91 desc')
                self.assertEqual(cmd.text, 'Cmd91 text')
            else:
                self.fail()

    def test_negative_load_commands_file_negative1(self):
        file_path = self.abs_path(__file__, 'config/negative/test_neg1_commands.xml')

        with self.assertRaises(InvalidConfigurationError) as ex:
            config._load_commands_file(file_path)

        self.assertTrue('Unexpected xml tag' in str(ex.exception))

    def _check_command_interface(self, cmd):
        # true: not None, not '' and not []
        # Command duck typing: .names, .desc, .text are mandatory
        self.assertTrue(cmd.names)
        for name in cmd.names:
            self.assertTrue(name)
        self.assertTrue(cmd.desc)
        self.assertTrue(cmd.text)
