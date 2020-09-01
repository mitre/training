from plugins.training.app.c_certification import Certification
from app.utility.base_object import BaseObject


class Exam(Certification, BaseObject):

    @property
    def display(self):
        return dict(name=self.name, description=self.description, badges=[b.display for b in self.badges],
                    cert_type=self.cert_type)

    def __init__(self, identifier, name, description, access):
        super().__init__(identifier, name, description, access)
        self.badges = []
        self.cert_type = 'exam'
