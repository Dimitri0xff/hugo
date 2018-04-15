import re

from bot import config
from bot.error import InvalidConfigurationError
from test.test_case_base import TestCaseBase


_TEST_CFG1 = "<commands> <simple desc='d'> <name str='n'></name> <response str='r'></response> </simple> </commands>"

_TEST_CFG2 = "<commands> <multiline desc='d'> <name str='n1'> <tag>tA</tag> </name> <name str='n2'></name>" \
             "<response str='r1'> <tag>tA</tag> </response> </multiline> </commands>"


class TestConfigNegative(TestCaseBase):

    _debug = False

    def _load_commands(self, xml_string, *expected_messages):
        with self.assertRaises(InvalidConfigurationError) as ex:
            config.load_commands_string(xml_string)

        ex_message = str(ex.exception)
        for msg in expected_messages:
            self.assertTrue(msg in ex_message,
                            'Expected "{}" in the error message, but it was "{}"'.format(msg, ex_message))

        if self._debug:
            print(ex_message)


    def test_simple_ok(self):
        config.load_commands_string(_TEST_CFG1)

    def test_unknown_command(self):
        self._load_commands(_TEST_CFG1.replace('simple', 'unknown_command'),
                            'Unexpected xml tag', 'unknown_command')

    def test_simple_empty_name(self):
        self._load_commands(_TEST_CFG1.replace("'n'", "''"),
                            'name', 'shall not be empty')

    def test_simple_name_with_space(self):
        self._load_commands(_TEST_CFG1.replace("'n'", "'hello there'"),
                            'name', 'space')

    def test_simple_no_name(self):
        self._load_commands(re.sub(r'<name.*name>', '', _TEST_CFG1),
                            'name', 'shall have at least one')

    def test_simple_no_response(self):
        self._load_commands(re.sub(r'<response.*response>', '', _TEST_CFG1),
                            'response', 'shall have exactly one')

    def test_simple_empty_response(self):
        self._load_commands(_TEST_CFG1.replace("'r'", "''"),
                            'response', 'shall not be empty')

    def test_simple_multiple_response(self):
        pos = _TEST_CFG1.find('</simple>')
        mod_test_config = _TEST_CFG1[:pos] + "<response str='r2'></response>" + _TEST_CFG1[pos:]
        self._load_commands(mod_test_config,
                            'response', 'shall have exactly one')

    def test_simple_extra_element(self):
        pos = _TEST_CFG1.find('</simple>')
        mod_test_config = _TEST_CFG1[:pos] + "<unkown_tag str='r3'></unkown_tag>" + _TEST_CFG1[pos:]
        self._load_commands(mod_test_config,
                            'Unexpected xml tag', 'unkown_tag')

    def test_simple_extra_text(self):
        pos = _TEST_CFG1.find('<name')
        mod_test_config = _TEST_CFG1[:pos] + " extra_text " + _TEST_CFG1[pos:]
        self._load_commands(mod_test_config,
                            'shall not have a text node', 'simple')

    # Multi-line

    def test_multiline_ok(self):
        config.load_commands_string(_TEST_CFG2)

    def test_multiline_empty_name(self):
        self._load_commands(_TEST_CFG2.replace("'n1'", "''"),
                            'name', 'shall not be empty')

    def test_multiline_name_with_space(self):
        self._load_commands(_TEST_CFG2.replace("'n1'", "'hello there'"),
                            'name', 'space')

    def test_multiline_no_name(self):
        self._load_commands(re.sub(r'<name.*name>', '', _TEST_CFG2),
                            'name', 'shall have at least one')

    def test_multiline_no_response(self):
        self._load_commands(re.sub(r'<response.*response>', '', _TEST_CFG2),
                            'response', 'shall have at least one')

    def test_multiline_empty_response(self):
        self._load_commands(_TEST_CFG2.replace("'r1'", "''"),
                            'response', 'shall not be empty')

    def test_multiline_empty_tag1(self):
        self._load_commands(_TEST_CFG2.replace("<tag>tA</tag> </name>", "<tag></tag> </name>"),
                            'tag', 'shall not be empty')

    def test_multiline_empty_tag2(self):
        self._load_commands(_TEST_CFG2.replace("<tag>tA</tag> </response>", "<tag></tag> </response>"),
                            'tag', 'shall not be empty')

    def test_multiline_extra_element(self):
        pos = _TEST_CFG2.find('</multiline>')
        mod_test_config = _TEST_CFG2[:pos] + "<unkown_tag str='r3'></unkown_tag>" + _TEST_CFG2[pos:]
        self._load_commands(mod_test_config,
                            'Unexpected xml tag', 'unkown_tag')

    def test_multiline_extra_text(self):
        pos = _TEST_CFG2.find('<name')
        mod_test_config = _TEST_CFG2[:pos] + " extra_text " + _TEST_CFG2[pos:]
        self._load_commands(mod_test_config,
                            'shall not have a text node', 'multiline')