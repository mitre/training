from app.utility.base_object import BaseObject


class Certification(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.identifier)

    @property
    def display(self):
        return dict(name=self.name, description=self.description, badges=[b.display for b in self.badges])

    def __init__(self, identifier, name, description, access):
        super().__init__()
        self.identifier = identifier
        self.name = name
        self.description = description
        self.access = access
        self.badges = []

    def store(self, ram):
        existing = self.retrieve(ram['certifications'], self.unique)
        if not existing:
            ram['certifications'].append(self)
            return self.retrieve(ram['certifications'], self.unique)
        return existing
