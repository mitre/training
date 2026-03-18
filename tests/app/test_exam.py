"""Tests for app.c_exam.Exam."""
import pytest

from plugins.training.app.c_exam import Exam
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_flag import Flag


class FakeFlag(Flag):
    name = "Exam Flag"
    challenge = "Exam challenge"
    extra_info = ""

    async def verify(self, services):
        return True


class TestExam:

    def _make_exam(self, **kw):
        defaults = dict(identifier="exam-1", name="Test Exam",
                        description="An exam", access="app")
        defaults.update(kw)
        return Exam(**defaults)

    def test_cert_type(self):
        e = self._make_exam()
        assert e.cert_type == 'exam'

    def test_display_includes_cert_type(self):
        e = self._make_exam()
        d = e.display
        assert 'cert_type' in d
        assert d['cert_type'] == 'exam'

    def test_display_has_name_and_description(self):
        e = self._make_exam(name="Final Exam", description="The big one")
        d = e.display
        assert d['name'] == 'Final Exam'
        assert d['description'] == 'The big one'

    def test_display_badges_empty(self):
        e = self._make_exam()
        assert e.display['badges'] == []

    def test_display_badges_with_content(self):
        e = self._make_exam()
        b = Badge(name="eb")
        b.flags.append(FakeFlag(number=1))
        e.badges.append(b)
        assert len(e.display['badges']) == 1

    def test_inherits_certification_methods(self):
        """Exam should have get_badge and get_flag from Certification."""
        e = self._make_exam()
        assert hasattr(e, 'get_badge')
        assert hasattr(e, 'get_flag')

    def test_unique_property(self):
        e = self._make_exam(identifier="u1")
        assert e.unique is not None

    def test_badges_initially_empty(self):
        e = self._make_exam()
        assert e.badges == []

    def test_store(self):
        e = self._make_exam()
        ram = {'certifications': []}
        e.store(ram)
        assert len(ram['certifications']) == 1
