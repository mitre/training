from plugins.training.app.c_flag import Flag
from app.utility.base_object import BaseObject


class MultipleChoice(Flag, BaseObject):

    def __init__(self, number, name, challenge, extra_info, verify, options, multi_select, flag_type):
        super().__init__(number, name, challenge, extra_info, verify)
        self.options = options
        self.multi_select = multi_select
        self.flag_type = flag_type

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, options=self.options,
                    multi_select=self.multi_select, flag_type=self.flag_type, completed=self.completed,
                    extra_info=self.extra_info, code=self.calculate_code(),
                    completed_ts=self.completed_ts.strftime('%Y-%m-%d %H:%M:%S') if self.completed_ts else '')
