

class SimpleCommand:

    def __init__(self, alias_names, desc, text):
        self.names = alias_names
        self.desc = desc
        self.text = text

    def message(self, message, command, args):
        return self.text

    def __repr__(self):
        return __class__.__name__ + ' ' + str(self.names)
