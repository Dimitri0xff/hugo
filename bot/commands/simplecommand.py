

class SimpleCommand:

    # TODO: regexp or dynamic name?
    def __init__(self, alias_names, desc):
        self.names = alias_names
        self.text = ''
        self.desc = desc

    # TODO: + sender, timestamp, channel etc?
    def message(self, command, args):
        return self.text
