import os
import xml.etree.ElementTree as ET

from bot.commands.multilinecommand import MultiLineCommand
from bot.commands.simplecommand import SimpleCommand
from bot.error import InvalidConfigurationError


# TODO: assert -> InvalidConfigurationException + filename + lxml sourceline?
def load_commands_folder(folder_path):
    loaded_commands = []
    for name in os.listdir(folder_path):
        path = os.path.join(folder_path, name)
        if not os.path.isfile(path):
            continue
        if name.endswith('command.xml') or name.endswith('commands.xml'):
            loaded_commands.extend(_load_commands_file(path))
    return loaded_commands


def _load_commands_file(file_path):
    commands = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    for node in root:
        if node.tag == 'simple':
            commands.append(_load_simple_command(node))
        elif node.tag == 'multiline':
            commands.append(_load_multiline_command(node))
        else:
            raise InvalidConfigurationError('Unexpected xml tag: "{}"'.format(node.tag))
    return commands


def _load_simple_command(node):
    names_str = _get_names_attrib(node)
    names_array = [name.strip() for name in names_str.split(';')]

    return SimpleCommand(names_array, node.attrib['desc'], node.text)


def _load_multiline_command(node):
    names_str = _get_names_attrib(node)
    names_array = []
    new_command = MultiLineCommand(node.attrib['desc'])

    for name_str in names_str.split(';'):
        name_str = name_str.strip()
        assert name_str.count('[') == 1, 'For a MultiLineCommand, name tags must contain exactly one ['
        assert name_str.count(']') == 1, 'For a MultiLineCommand, name tags must contain exactly one ]'
        assert name_str[-1] == ']', 'For a MultiLineCommand, name tags string shall end with ]'
        if '[]' in name_str:
            name = name_str.replace('[]', '')
            tags = set()
        else:
            name_str = name_str.replace(']', '')
            name, tags_str = name_str.split('[', maxsplit=1)
            assert ';' not in tags_str, 'Use | for separator'
            tags = {tag.strip() for tag in tags_str.split('|')}
        new_command.add_name(name, tags)

    assert len(node) > 0, 'Response must contain any lines'
    for line in node:
        assert line.tag == 'line', 'Unexpected tag: {}'.format(line.tag)
        tags_str = line.attrib['tags']
        tags = {tag.strip() for tag in tags_str.split(';')}
        new_command.add_line(line.text, tags)

    return new_command


def _get_names_attrib(node):
    names_str = node.attrib['names']
    assert ',' not in names_str, 'Use ; for separator'
    return names_str
