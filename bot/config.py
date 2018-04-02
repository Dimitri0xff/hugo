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
            loaded_commands.extend(load_commands_file(path))
    return loaded_commands


def load_commands_string(xml_string):
    root = ET.fromstring(xml_string)
    return _load_commands(root)


def load_commands_file(file_path):
    tree = ET.parse(file_path)
    return _load_commands(tree.getroot())


def _load_commands(root):
    commands = []
    for node in root:
        if node.tag == 'simple':
            commands.append(_load_simple_command(node))
        elif node.tag == 'multiline':
            commands.append(_load_multiline_command(node))
        else:
            raise InvalidConfigurationError('Unexpected xml tag: "{}"'.format(node.tag))
    return commands


def _load_simple_command(node):

    if len(node) > 0:
        raise InvalidConfigurationError('A SimpleCommand shall not have any child nodes')

    names_str = node.attrib['names']
    if ',' in names_str:
        raise InvalidConfigurationError('In a "names" attribute use ; for separator instead of comma. Attribute value: '
                                        + names_str)

    names_array = [name.strip() for name in names_str.split(';')]
    if len(names_array) == 1 and not names_array[0]:
        raise InvalidConfigurationError('The "names" attribute of a Command shall not be empty')
    names_array_as_str = str(names_array)
    for name in names_array:
        _check_name(name, names_array_as_str)

    if not node.text:
        raise InvalidConfigurationError('The text (response) of a Command shall not be empty')

    return SimpleCommand(names_array, node.attrib['desc'], node.text)


def _load_multiline_command(node):
    names_str = node.attrib['names']
    if ',' in names_str:
        # Make sure the invalid character is not in a name tag,
        # then it should be caught later with a different error message
        before, after = names_str.split(',', maxsplit=1)
        if '[' not in before.split(']')[-1]:
            raise InvalidConfigurationError('In a "names" attribute use ; for separator instead of comma. Attribute value: '
                                            + names_str)

    names_array = []
    new_command = MultiLineCommand(node.attrib['desc'])

    if node.text and node.text.strip():
        raise InvalidConfigurationError('A MultiLineCommand tag shall not have text node')

    for name_str in names_str.split(';'):
        name_str = name_str.strip()
        if name_str.count('[') != 1:
            raise InvalidConfigurationError('For a MultiLineCommand, name tags must contain exactly one [')
        if name_str.count(']') != 1:
            raise InvalidConfigurationError('For a MultiLineCommand, name tags must contain exactly one ]. Current value: ' + name_str)
        if name_str[-1] != ']':
            raise InvalidConfigurationError('For a MultiLineCommand, name tags string shall end with ]')
        if '[]' in name_str:
            name = name_str.replace('[]', '')
            tags = set()
        else:
            name_str = name_str.replace(']', '')
            name, tags_str = name_str.split('[', maxsplit=1)
            if ',' in tags_str:
                raise InvalidConfigurationError('Use | for separator. Tag value: ' + tags_str)
            tags = {tag.strip() for tag in tags_str.split('|')}

        _check_name(name, names_str)
        new_command.add_name(name, tags)

    if len(node) == 0:
        raise InvalidConfigurationError('Response must contain any lines')

    for line in node:
        if line.tag != 'line':
            raise InvalidConfigurationError('Unexpected tag: {}'.format(line.tag))
        tags_str = line.attrib['tags']
        if ',' in tags_str or '|' in tags_str:
            raise InvalidConfigurationError('Use ; for separator: ' + tags_str)
        tags = {tag.strip() for tag in tags_str.split(';')}
        new_command.add_line(line.text, tags)

    return new_command


def _check_name(name, names):
    if not name:
        raise InvalidConfigurationError('No element in the "names" attribute shall be empty: ' + names)
    if ' ' in name:
        raise InvalidConfigurationError('A command name shall not contain any spaces, current name: "{}"'.format(name))
