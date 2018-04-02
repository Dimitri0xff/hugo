from bot import config
from bot.error import InvalidConfigurationError
from test.test_case_base import TestCaseBase


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


    def test_unknown_tag(self):
        self._load_commands("<commands> <unknowntag names='n' desc='d'>t</unknowntag> </commands>",
                            'Unexpected xml tag', 'unknowntag')

    def test_simple_name_separator(self):
        self._load_commands("<commands> <simple names='n1; n2, n3' desc='d'>t</simple> </commands>",
                            'use ; for separator', 'n1; n2, n3')

    def test_simple_empty_name(self):
        self._load_commands("<commands> <simple names='' desc='d'>t</simple> </commands>",
                            'name', 'shall not be empty')

    def test_simple_name_with_space(self):
        self._load_commands("<commands> <simple names='hello there' desc='d'>t</simple> </commands>",
                            'name', 'space')

    def test_simple_empty_name_element(self):
        self._load_commands("<commands> <simple names='n1; ; n2' desc='d'>t</simple> </commands>",
                            'name', 'empty')

    def test_simple_empty_text(self):
        self._load_commands("<commands> <simple names='n1' desc='d'></simple> </commands>",
                            'text', 'shall not be empty')

    def test_simple_child_node(self):
        self._load_commands("<commands> <simple names='n1' desc='d'>t <line>l</line></simple> </commands>",
                            'shall not have any child nodes')

    def test_multiline_no_name_tag(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2' desc='d'>" \
                            "<line tags='tA'>l1</line> </multiline> </commands>",
                            'name tag')

    def test_multiline_name_with_Space(self):
        self._load_commands("<commands> <multiline names='n1a n[tA]' desc='d'>" \
                            "<line tags='tA'>l1</line> </multiline> </commands>",
                            'name', 'space')

    def test_multiline_name_tag_not_closed(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB; n3[tC]' desc='d'>" \
                            "<line tags='tA'>l1</line> </multiline> </commands>",
                            'name tag')

    def test_multiline_name_tag_extra_text(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB]abc' desc='d'>" \
                            "<line tags='tA'>l1</line> </multiline> </commands>",
                            'name tag')

    def test_multiline_name_tag_no_name(self):
        self._load_commands("<commands> <multiline names='n1[tA]; [tB]' desc='d'>" \
                            "<line tags='tA'>l1</line> </multiline> </commands>",
                            'empty')

    def test_multiline_no_lines(self):
        self._load_commands("<commands> <multiline names='n1[tA]' desc='d'> </multiline> </commands>",
                            'must contain any lines')

    def test_multiline_with_text(self):
        self._load_commands("<commands> <multiline names='n1[tA]' desc='d'>" \
                            "text <line tags='tA'>l1</line></multiline> </commands>",
                            'shall not', 'text node')

    def test_multiline_name_separator1(self):
        self._load_commands("<commands> <multiline names='n1[tA], n2[tB]' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'use ; for separator', 'n1[tA], n2[tB]')

    def test_multiline_name_separator2(self):
        self._load_commands("<commands> <multiline names='n1,' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'use ; for separator', 'n1,')

    def test_multiline_name_separator3(self):
        self._load_commands("<commands> <multiline names=', n1' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'use ; for separator', ', n1')

    def test_multiline_name_separator4(self):
        self._load_commands("<commands> <multiline names='n1[], n2[], n3[]' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'use ; for separator', 'n1[], n2[], n3[]')

    def test_multiline_name_tag_separator1(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB;tC]' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'n2[tB')

    def test_multiline_name_tag_separator2(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB,tC]' desc='d'>" \
                            "<line tags='tA'>l1</line></multiline> </commands>",
                            'Use | for separator', 'tB,tC')

    def test_multiline_tag_separator1(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB]' desc='d'>" \
                            "<line tags='tA, tB'>l1</line></multiline> </commands>",
                            'Use ; for separator', 'tA, tB')

    def test_multiline_tag_separator2(self):
        self._load_commands("<commands> <multiline names='n1[tA]; n2[tB]' desc='d'>" \
                            "<line tags='tA|tB'>l1</line></multiline> </commands>",
                            'Use ; for separator', 'tA|tB')

    def test_multiline_unknowntag(self):
        self._load_commands("<commands> <multiline names='n1[tA]' desc='d'> <line tags='tA'>l1</line> " \
                            "<unknowntag>t</unknowntag></multiline> </commands> ",
                            'Unexpected tag', 'unknowntag')
