
class MultiLineCommand:

    def __init__(self, desc):
        self.names = []
        self._name_tags = {}
        self.desc = desc
        self._lines = []

    def add_name(self, name, tags):
        assert type(tags) is set, 'unexpected type: {}'.format(type(tags).__name__)
        self.names.append(name)
        self._name_tags[name] = tags

    def add_line(self, text, tags):
        assert type(tags) is set, 'unexpected type: {}'.format(type(tags).__name__)
        self._lines.append(_Line(text, tags))

    @property
    def text(self):
        return '\n'.join(line.text for line in self._lines)

    async def message(self, client, message, command, args):
        tags = self._name_tags[command]
        if not tags:
            filtered_lines = self._lines
        else:
            # '' should match all tags
            filtered_lines = [line for line in self._lines if line.tags == {''} or bool(tags & line.tags)]
        # todo: cache text per name
        response = '\n'.join(line.text for line in filtered_lines)
        await client.send_message(message.channel, response)

    def __repr__(self):
        return __class__.__name__ + ' ' + str(self.names)


class _Line:
    """An entry with tags. If one or more tag matches, the entry shall be printed"""
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags
