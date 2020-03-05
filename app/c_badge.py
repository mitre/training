from app.utility.base_object import BaseObject


class Badge(BaseObject):

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
