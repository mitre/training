from plugins.training.app.c_flag import Flag
from app.utility.base_object import BaseObject


class FillInBlank(Flag, BaseObject):

    def __init__(self, number, name, challenge, answer, extra_info=None):
        super().__init__(number, name, challenge, extra_info, self.verify)
        self.answer = answer
        self.flag_type = 'fillinblank'

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, flag_type=self.flag_type,
                    completed=self.completed, extra_info=self.extra_info, code=self.calculate_code(),
                    completed_ts=self.completed_ts.strftime('%Y-%m-%d %H:%M:%S') if self.completed_ts else '')

    def verify(self, answer):
        return answer.lower() == self.answer
