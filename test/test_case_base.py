from unittest import TestCase

import os

from bot import utils


class TestCaseBase(TestCase):

    def abs_path(self, file, rel_path):
        return utils.abs_path(file, rel_path)
