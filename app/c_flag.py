from app.utility.base_object import BaseObject


class Flag(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, completed=self.completed)

    def __init__(self, number, name, challenge, verify):
        super().__init__()
        self.number = number
        self.name = name
        self.challenge = challenge
        self.verify = verify
        self.completed = False

    def store(self, ram):
        existing = self.retrieve(ram['flags'], self.unique)
        if not existing:
            ram['flags'].append(self)
            return self.retrieve(ram['flags'], self.unique)
        return existing
