from app.utility.base_object import BaseObject


class Certification(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def display(self):
        return dict(name=self.name, badges=[b.display for b in self.badges])

    def __init__(self, name, access):
        super().__init__()
        self.name = name
        self.access = access
        self.badges = []

    def store(self, ram):
        existing = self.retrieve(ram['certifications'], self.unique)
        if not existing:
            ram['certifications'].append(self)
            return self.retrieve(ram['certifications'], self.unique)
        return existing
