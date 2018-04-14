

class SimpleCommand:

    def __init__(self, alias_names, desc, text):
        self.names = alias_names
        self.desc = desc
        self.text = text

    async def message(self, client, message, command, args):
        await client.send_message(message.channel, self.text)

    def __repr__(self):
        return __class__.__name__ + ' ' + str(self.names)
