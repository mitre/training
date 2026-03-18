"""Tests for app.c_fillinblank.FillInBlank."""
import pytest

from plugins.training.app.c_fillinblank import FillInBlank


class ConcreteFIB(FillInBlank):
    name = 'FIB Test'
    challenge = 'Fill in the blank'
    extra_info = ''
    answer = 'correct'


class TestFillInBlank:

    def test_flag_type(self):
        f = ConcreteFIB(number=1)
        assert f.flag_type == 'fillinblank'

    def test_verify_correct_answer(self):
        f = ConcreteFIB(number=1)
        assert f.verify('correct') is True

    def test_verify_case_insensitive(self):
        f = ConcreteFIB(number=1)
        assert f.verify('CORRECT') is True
        assert f.verify('Correct') is True

    def test_verify_wrong_answer(self):
        f = ConcreteFIB(number=1)
        assert f.verify('wrong') is False

    def test_verify_empty_string(self):
        f = ConcreteFIB(number=1)
        assert f.verify('') is False

    def test_display_keys(self):
        f = ConcreteFIB(number=1)
        d = f.display
        assert 'flag_type' in d
        assert 'number' in d
        assert 'name' in d
        assert 'challenge' in d
        assert 'completed' in d
        assert 'code' in d

    def test_display_flag_type_value(self):
        f = ConcreteFIB(number=1)
        assert f.display['flag_type'] == 'fillinblank'

    def test_inherits_flag(self):
        from plugins.training.app.c_flag import Flag
        assert issubclass(FillInBlank, Flag)

    def test_has_answer_attribute(self):
        f = ConcreteFIB(number=1)
        assert hasattr(f, 'answer')
