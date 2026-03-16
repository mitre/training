"""Tests for app.c_navigator.Navigator."""
import json
import pytest

from plugins.training.app.c_navigator import Navigator


class ConcreteNav(Navigator):
    name = 'Nav Test'
    challenge = 'Upload layer'
    extra_info = ''
    answer = [('initial-access', 'T1190'), ('execution', 'T1059')]


class TestNavigator:

    def test_flag_type(self):
        f = ConcreteNav(number=1)
        assert f.flag_type == 'navigator'

    def test_verify_correct_layer(self):
        f = ConcreteNav(number=1)
        layer = json.dumps({
            'techniques': [
                {'tactic': 'initial-access', 'techniqueID': 'T1190'},
                {'tactic': 'execution', 'techniqueID': 'T1059'},
            ]
        })
        assert f.verify(layer) is True

    def test_verify_wrong_layer(self):
        f = ConcreteNav(number=1)
        layer = json.dumps({
            'techniques': [
                {'tactic': 'initial-access', 'techniqueID': 'T9999'},
            ]
        })
        assert f.verify(layer) is False

    def test_verify_empty_techniques(self):
        f = ConcreteNav(number=1)
        layer = json.dumps({'techniques': []})
        assert f.verify(layer) is False

    def test_verify_extra_techniques_fail(self):
        f = ConcreteNav(number=1)
        layer = json.dumps({
            'techniques': [
                {'tactic': 'initial-access', 'techniqueID': 'T1190'},
                {'tactic': 'execution', 'techniqueID': 'T1059'},
                {'tactic': 'persistence', 'techniqueID': 'T1053'},
            ]
        })
        assert f.verify(layer) is False

    def test_verify_order_independent(self):
        f = ConcreteNav(number=1)
        layer = json.dumps({
            'techniques': [
                {'tactic': 'execution', 'techniqueID': 'T1059'},
                {'tactic': 'initial-access', 'techniqueID': 'T1190'},
            ]
        })
        assert f.verify(layer) is True

    def test_sort_tactic_technique(self):
        input_list = [('tactic_a', 'T002'), ('tactic_a', 'T001'), ('tactic_b', 'T003')]
        result = Navigator._sort_tactic_technique(input_list)
        assert result == {'tactic_a': ['T001', 'T002'], 'tactic_b': ['T003']}

    def test_sort_tactic_technique_empty(self):
        result = Navigator._sort_tactic_technique([])
        assert result == {}

    def test_display_has_flag_type(self):
        f = ConcreteNav(number=1)
        assert f.display['flag_type'] == 'navigator'

    def test_inherits_flag(self):
        from plugins.training.app.c_flag import Flag
        assert issubclass(Navigator, Flag)

    def test_verify_invalid_json_raises(self):
        f = ConcreteNav(number=1)
        with pytest.raises(json.JSONDecodeError):
            f.verify('not json')

    def test_verify_duplicate_tactics(self):
        """Multiple techniques under same tactic must all match."""
        class MultiTechNav(Navigator):
            name = 'Multi'
            challenge = ''
            extra_info = ''
            answer = [('tactic_a', 'T001'), ('tactic_a', 'T002')]

        f = MultiTechNav(number=1)
        layer = json.dumps({
            'techniques': [
                {'tactic': 'tactic_a', 'techniqueID': 'T001'},
                {'tactic': 'tactic_a', 'techniqueID': 'T002'},
            ]
        })
        assert f.verify(layer) is True
