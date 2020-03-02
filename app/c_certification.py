from app.utility.base_object import BaseObject


class Certification(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def display(self):
        return dict(name=self.name, flags=[f.display for f in self.flags])

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.flags = []

    def store(self, ram):
        existing = self.retrieve(ram['certification'], self.unique)
        if not existing:
            ram['certification'].append(self)
            return self.retrieve(ram['certification'], self.unique)
        return existing
