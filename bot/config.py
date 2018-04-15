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
    for element in root:
        if element.tag == 'simple':
            commands.append(_load_simple_command(element))
        elif element.tag == 'multiline':
            commands.append(_load_multiline_command(element))
        else:
            raise InvalidConfigurationError('Unexpected xml tag: "{}"'.format(element.tag))
    return commands


def _load_simple_command(command):
    _check_child_elements(command, 'name', 'response')
    _check_no_text(command)

    for element in command:
        if element.tag != 'name' and element.tag != 'response':
            raise InvalidConfigurationError('Unexpected xml tag: "{}"'.format(element.tag))

    name_elements = command.findall('name')
    if not name_elements:
        raise InvalidConfigurationError('<{}> element shall have at least one <name> child element'.format(command.tag))

    names_list = []
    for name in name_elements:
        _check_no_text(name)
        name_str = _get_attrib(name, 'str')
        _check_name(name_str)
        names_list.append(name_str)

    response_elements = command.findall('response')
    if len(response_elements) != 1:
        raise InvalidConfigurationError('<{}> element shall have exactly one <response> child element'.format(command.tag))

    response = response_elements[0]
    _check_no_text(response)
    response_str = _get_attrib(response, 'str')

    desc = _get_attrib(command, 'desc')

    return SimpleCommand(names_list, desc, response_str)


def _load_multiline_command(command):
    _check_child_elements(command, 'name', 'response')
    _check_no_text(command)

    name_elements = command.findall('name')
    if not name_elements:
        raise InvalidConfigurationError('<{}> element shall have at least one <name> child element'.format(command.tag))

    desc = _get_attrib(command, 'desc')
    new_command = MultiLineCommand(desc)

    for name in name_elements:
        _check_no_text(name)
        tags = set()
        name_str = _get_attrib(name, 'str')
        _check_name(name_str)

        for tag in name:
            tag_text = _get_text(tag)
            tags.add(tag_text)

        new_command.add_name(name_str, tags)

    response_elements = command.findall('response')
    if not response_elements:
        raise InvalidConfigurationError('<{}> element shall have at least one <response> child element'.format(command.tag))

    for response in response_elements:
        _check_no_text(response)
        tags = set()
        response_str = _get_attrib(response, 'str')

        for tag in response:
            tag_text = _get_text(tag)
            tags.add(tag_text)

        new_command.add_response(response_str, tags)

    return new_command


def _check_name(name):
    if ' ' in name:
        raise InvalidConfigurationError('A command name shall not contain any spaces, current name: "{}"'.format(name))


def _get_attrib(element, attrib_name):
    attrib = element.attrib.get(attrib_name)
    if attrib is None:
        raise InvalidConfigurationError('<{}> element must have "{}" attribute'.format(element.tag, attrib_name))
    attrib = attrib.strip()
    if not attrib:
        raise InvalidConfigurationError('"{}" attribute of <{}> shall not be empty'.format(attrib_name, element.tag))
    return attrib


def _get_text(element):
    text = element.text
    if text:
        text = text.strip()
    if not text:
        raise InvalidConfigurationError('Text node of a <{}> element shall not be empty'.format(element.tag))
    return text


def _check_child_elements(element, *allowed_tags):
    for child in element:
        if not child.tag in allowed_tags:
            raise InvalidConfigurationError('Unexpected xml tag: "{}"'.format(child.tag))


def _check_no_text(element):
    text = element.text
    if text:
        text = text.strip()
    if text:
        raise InvalidConfigurationError('Element <{}> shall not have a text node'.format(element.tag))
