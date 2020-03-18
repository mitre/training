from plugins.training.app.c_flag import Flag


def calculate_code(self):
    if self.started_ts and self.completed_ts:
        return '%d+%d+%d@' % (self.number, abs((self.completed_ts - self.started_ts).seconds), self._ticks)
    return '%d+0+%d@' % (self.number, self._ticks)


Flag.calculate_code = calculate_code
