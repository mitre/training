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
        self._completed_ts = datetime.now()

    @property
    def completed_ts(self):
        return self._completed_ts

    @property
    def started_ts(self):
        return self._started_ts

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, completed=self.completed,
                    extra_info=self.extra_info, code=self.calculate_code(),
                    completed_ts=self.completed_ts.strftime('%Y-%m-%d %H:%M:%S') if self.completed_ts else '')

    def __init__(self, number, name, challenge, extra_info, verify, setup, prerequisites_met):
        super().__init__()
        self.number = number
        self.name = name
        self.challenge = challenge
        self.extra_info = extra_info
        self.verify = verify
        self.prerequisites_met = prerequisites_met
        self.setup = setup
        self.setup_fields = None
        self._completed = False
        self._completed_ts = None
        self._started_ts = None
        self._ticks = 0

    def store(self, ram):
        existing = self.retrieve(ram['flags'], self.unique)
        if not existing:
            ram['flags'].append(self)
            return self.retrieve(ram['flags'], self.unique)
        return existing

    async def activate(self, services):
        if not self._started_ts:
            if self.prerequisites_met is not None and not await self.prerequisites_met(services):
                return False
            self._started_ts = datetime.now()
            if self.setup:
                self.setup_fields = await self.setup(services)
        if not self._completed_ts:
            self._ticks += 1
        return True

    def calculate_code(self):
        return self.unique
