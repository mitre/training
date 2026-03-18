"""Exhaustive tests for app.c_badge.Badge."""
import pytest

from plugins.training.app import errors
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_flag import Flag


class FakeFlag(Flag):
    name = "Test Flag"
    challenge = "Run the tests"
    extra_info = "Need to use pytest to run the tests"

    async def verify(self, services):
        return True


class AnotherFlag(Flag):
    name = "Another Flag"
    challenge = "Another challenge"
    extra_info = ""

    async def verify(self, services):
        return False


class TestBadge:

    def test_find_flag(self):
        badge1 = Badge(name="foo-badge-1")
        flag1 = FakeFlag(number=1)
        badge1.flags.append(flag1)
        found = badge1.get_flag(flag_name=flag1.name)
        assert found is flag1

    def test_find_flag_fail(self):
        badge1 = Badge(name="foo-badge-1")
        flag1 = FakeFlag(number=1)
        badge1.flags.append(flag1)

        with pytest.raises(errors.FlagDoesNotExist):
            badge1.get_flag(flag_name='DOES NOT EXIST')

    def test_badge_name(self):
        badge = Badge(name="my-badge")
        assert badge.name == "my-badge"

    def test_badge_flags_initially_empty(self):
        badge = Badge(name="empty")
        assert badge.flags == []

    def test_badge_unique_property(self):
        badge = Badge(name="unique-test")
        assert badge.unique is not None
        assert isinstance(badge.unique, str)

    def test_badge_unique_deterministic(self):
        b1 = Badge(name="same")
        b2 = Badge(name="same")
        assert b1.unique == b2.unique

    def test_badge_unique_differs_for_different_names(self):
        b1 = Badge(name="alpha")
        b2 = Badge(name="beta")
        assert b1.unique != b2.unique

    def test_badge_display(self):
        badge = Badge(name="display-badge")
        flag = FakeFlag(number=1)
        badge.flags.append(flag)
        d = badge.display
        assert d['name'] == 'display-badge'
        assert isinstance(d['flags'], list)
        assert len(d['flags']) == 1

    def test_badge_display_empty_flags(self):
        badge = Badge(name="no-flags")
        d = badge.display
        assert d['flags'] == []

    def test_multiple_flags_get_correct_one(self):
        badge = Badge(name="multi")
        f1 = FakeFlag(number=1)
        f2 = AnotherFlag(number=2)
        badge.flags.extend([f1, f2])
        assert badge.get_flag("Test Flag") is f1
        assert badge.get_flag("Another Flag") is f2

    def test_get_flag_returns_first_match(self):
        """If two flags share the same name (unusual but possible), get first."""
        badge = Badge(name="dup")
        f1 = FakeFlag(number=1)
        f2 = FakeFlag(number=2)
        badge.flags.extend([f1, f2])
        assert badge.get_flag("Test Flag") is f1

    def test_display_includes_all_flags(self):
        badge = Badge(name="many")
        for i in range(5):
            badge.flags.append(FakeFlag(number=i))
        assert len(badge.display['flags']) == 5
