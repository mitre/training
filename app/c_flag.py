from datetime import datetime

from app.utility.base_object import BaseObject


class Flag(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, v):
        self._completed = v
        self._completed_timestamp = datetime.now()

    @property
    def completed_timestamp(self):
        return self._completed_timestamp

    @property
    def started_ts(self):
        return self._started_ts

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, completed=self.completed,
                    extra_info=self.extra_info, code=self.calculate_code(),
                    completed_timestamp=self._convert_timestamp())

    def __init__(self, number, name, challenge, verify, extra_info=''):
        super().__init__()
        self.number = number
        self.name = name
        self.challenge = challenge
        self.extra_info = extra_info
        self.verify = verify
        self._completed = False
        self._completed_timestamp = None
        self._started_ts = None
        self._ticks = 0

    def store(self, ram):
        existing = self.retrieve(ram['flags'], self.unique)
        if not existing:
            ram['flags'].append(self)
            return self.retrieve(ram['flags'], self.unique)
        return existing

    def activate(self):
        if not self._started_ts:
            self._started_ts = datetime.now()
        if not self._completed_timestamp:
            self._ticks += 1

    def calculate_code(self):
        return self.unique

    def _convert_timestamp(self):
        return self.completed_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.completed_timestamp else ''
