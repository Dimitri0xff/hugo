import os
import xml.etree.ElementTree as ET


def load_commands(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    # FIXME
    return ''
