from unittest import TestCase

import os


class TestCaseBase(TestCase):

    def abs_path(self, file, rel_path):
        dir_path = os.path.dirname(os.path.abspath(file))
        return dir_path + '/' + rel_path;
