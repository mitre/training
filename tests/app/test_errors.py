"""Tests for app.errors module."""
import pytest

from plugins.training.app.errors import ObjectDoesNotExist, BadgeDoesNotExist, FlagDoesNotExist


class TestErrors:

    def test_object_does_not_exist_is_exception(self):
        assert issubclass(ObjectDoesNotExist, Exception)

    def test_badge_does_not_exist_inherits(self):
        assert issubclass(BadgeDoesNotExist, ObjectDoesNotExist)

    def test_flag_does_not_exist_inherits(self):
        assert issubclass(FlagDoesNotExist, ObjectDoesNotExist)

    def test_badge_does_not_exist_is_exception(self):
        assert issubclass(BadgeDoesNotExist, Exception)

    def test_flag_does_not_exist_is_exception(self):
        assert issubclass(FlagDoesNotExist, Exception)

    def test_raise_badge(self):
        with pytest.raises(BadgeDoesNotExist):
            raise BadgeDoesNotExist()

    def test_raise_flag(self):
        with pytest.raises(FlagDoesNotExist):
            raise FlagDoesNotExist()

    def test_catch_as_parent(self):
        with pytest.raises(ObjectDoesNotExist):
            raise BadgeDoesNotExist()

        with pytest.raises(ObjectDoesNotExist):
            raise FlagDoesNotExist()

    def test_exception_message(self):
        err = BadgeDoesNotExist("missing badge")
        assert str(err) == "missing badge"
