import abc

from datetime import datetime

from app.utility.base_object import BaseObject


class RegisterLeafClasses(type):
    # https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Metaprogramming.html#example-self-registration-of-subclasses
    def __init__(cls, name, bases, nmspc):
        super(RegisterLeafClasses, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = dict()
        if cls not in cls.registry.keys():
            cls.registry[cls] = dict(module_name=cls.__module__)
        if bases[0] in cls.registry.keys():
            cls.registry.pop(bases[0])


class Flag(BaseObject, metaclass=RegisterLeafClasses):

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
                    completed_timestamp=self._convert_timestamp(),
                    resettable='True' if self.additional_fields and 'adversary_id' in self.additional_fields
                    else 'False')

    def __init__(self, number, name, challenge, extra_info='', additional_fields=None):
        super().__init__()
        self.number = number
        self.name = name
        self.challenge = challenge
        self.extra_info = extra_info
        self.additional_fields = additional_fields
        self._completed = False
        self._completed_timestamp = None
        self._started_ts = None
        self._ticks = 0

    @abc.abstractmethod
    def verify(self, services):
        """
        Determines whether a flag's challenge has been met or not
        :param services:
        :return: boolean True if flag challenge is met, False otherwise
        """
        pass

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

    @staticmethod
    def _is_unauth_process_killed(op):
        return op.ran_ability_id('02fb7fa9-8886-4330-9e65-fa7bb1bc5271')

    @staticmethod
    def _is_unauth_process_detected(op):
        return all(trait in [f.trait for f in op.all_facts()] for trait in
                   ['remote.port.unauthorized', 'host.pid.unauthorized']) and \
               op.ran_ability_id('3b4640bc-eacb-407a-a997-105e39788781')

    @staticmethod
    def _is_file_found(op):
        return all(trait in [f.trait for f in op.all_facts()] for trait in
                   ['file.malicious.hash', 'host.malicious.file']) and \
               op.ran_ability_id('f9b3eff0-e11c-48de-9338-1578b351b14b')
