"""Tests for app.c_multiplechoice.MultipleChoice."""
import pytest

from plugins.training.app.c_multiplechoice import MultipleChoice


class ConcreteMC(MultipleChoice):
    name = 'MC Test'
    challenge = 'Pick the right one'
    extra_info = ''
    answer = 'B'
    options = ['A', 'B', 'C', 'D']


class MultiSelectMC(MultipleChoice):
    name = 'Multi MC'
    challenge = 'Pick all'
    extra_info = ''
    answer = ['A', 'C']
    options = ['A', 'B', 'C', 'D']
    multi_select = True


class TestMultipleChoice:

    def test_flag_type(self):
        f = ConcreteMC(number=1)
        assert f.flag_type == 'multiplechoice'

    def test_verify_correct(self):
        f = ConcreteMC(number=1)
        assert f.verify('B') is True

    def test_verify_wrong(self):
        f = ConcreteMC(number=1)
        assert f.verify('A') is False

    def test_verify_case_sensitive(self):
        f = ConcreteMC(number=1)
        assert f.verify('b') is False

    def test_verify_multi_select_correct(self):
        f = MultiSelectMC(number=1)
        assert f.verify(['A', 'C']) is True

    def test_verify_multi_select_wrong(self):
        f = MultiSelectMC(number=1)
        assert f.verify(['A', 'B']) is False

    def test_display_keys(self):
        f = ConcreteMC(number=1)
        d = f.display
        assert 'flag_type' in d
        assert 'options' in d
        assert 'multi_select' in d

    def test_display_options(self):
        f = ConcreteMC(number=1)
        assert f.display['options'] == ['A', 'B', 'C', 'D']

    def test_multi_select_default_false(self):
        f = ConcreteMC(number=1)
        assert f.multi_select is False

    def test_multi_select_true(self):
        f = MultiSelectMC(number=1)
        assert f.multi_select is True

    def test_inherits_flag(self):
        from plugins.training.app.c_flag import Flag
        assert issubclass(MultipleChoice, Flag)
