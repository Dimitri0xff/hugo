from bot import config
from test.test_case_base import TestCaseBase


class TestConfig(TestCaseBase):

    def test_xml(self):
        file_path = self.abs_path(__file__, '../../config/bot/commands.xml')
        commands = config.load_commands(file_path)
        self.assertIsNotNone(commands)
