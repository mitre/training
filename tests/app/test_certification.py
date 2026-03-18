"""Exhaustive tests for app.c_certification.Certification."""
import pytest

from plugins.training.app import errors
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_flag import Flag
from plugins.training.app.c_certification import Certification


class FakeFlag(Flag):
    name = "Test Flag"
    challenge = "Run the tests"
    extra_info = "Need to use pytest to run the tests"

    async def verify(self, services):
        return True


class TestCertification:

    def _make_cert(self, **kw):
        defaults = dict(identifier="foo", name="test-certification",
                        description="used for tests", access="red")
        defaults.update(kw)
        return Certification(**defaults)

    def test_find_badge(self):
        cert = self._make_cert()
        badge1 = Badge(name="foo-badge-1")
        badge2 = Badge(name="foo-badge-2")
        cert.badges.extend([badge1, badge2])
        found = cert.get_badge("foo-badge-1")
        assert found is badge1

    def test_find_badge_fail(self):
        cert = self._make_cert()
        cert.badges.append(Badge(name="foo-badge-1"))
        with pytest.raises(errors.BadgeDoesNotExist):
            cert.get_badge("DOES NOT EXIST")

    def test_find_flag(self):
        cert = self._make_cert()
        badge1 = Badge(name="foo-badge-1")
        flag1 = FakeFlag(number=1)
        badge1.flags.append(flag1)
        cert.badges.append(badge1)
        found = cert.get_flag(badge_name=badge1.name, flag_name=flag1.name)
        assert found is flag1

    def test_find_flag_fail(self):
        cert = self._make_cert()
        badge1 = Badge(name="foo-badge-1")
        flag1 = FakeFlag(number=1)
        badge1.flags.append(flag1)
        cert.badges.append(badge1)

        with pytest.raises(errors.BadgeDoesNotExist):
            cert.get_flag(badge_name='DOES NOT EXIST', flag_name=flag1.name)

        with pytest.raises(errors.FlagDoesNotExist):
            cert.get_flag(badge_name=badge1.name, flag_name='DOES NOT EXIST')

    # --- Additional exhaustive tests ---

    def test_unique_property(self):
        cert = self._make_cert(identifier="abc")
        assert cert.unique is not None
        assert isinstance(cert.unique, str)

    def test_unique_deterministic(self):
        c1 = self._make_cert(identifier="same")
        c2 = self._make_cert(identifier="same")
        assert c1.unique == c2.unique

    def test_unique_differs_for_different_ids(self):
        c1 = self._make_cert(identifier="aaa")
        c2 = self._make_cert(identifier="bbb")
        assert c1.unique != c2.unique

    def test_display_property(self):
        cert = self._make_cert(name="My Cert", description="desc")
        d = cert.display
        assert d['name'] == 'My Cert'
        assert d['description'] == 'desc'
        assert d['badges'] == []

    def test_display_with_badges(self):
        cert = self._make_cert()
        b = Badge(name="b1")
        b.flags.append(FakeFlag(number=1))
        cert.badges.append(b)
        d = cert.display
        assert len(d['badges']) == 1
        assert d['badges'][0]['name'] == 'b1'

    def test_initial_badges_empty(self):
        cert = self._make_cert()
        assert cert.badges == []

    def test_name_and_description_stored(self):
        cert = self._make_cert(name="N", description="D")
        assert cert.name == "N"
        assert cert.description == "D"

    def test_access_stored(self):
        cert = self._make_cert(access="blue")
        assert cert.access == "blue"

    def test_store_method(self):
        cert = self._make_cert(identifier="store-test")
        ram = {'certifications': []}
        result = cert.store(ram)
        assert result is not None
        assert len(ram['certifications']) == 1

    def test_store_idempotent(self):
        cert = self._make_cert(identifier="idem")
        ram = {'certifications': []}
        cert.store(ram)
        cert.store(ram)
        assert len(ram['certifications']) == 1

    def test_get_badge_returns_correct_among_many(self):
        cert = self._make_cert()
        for i in range(10):
            cert.badges.append(Badge(name=f"badge-{i}"))
        found = cert.get_badge("badge-7")
        assert found.name == "badge-7"

    def test_get_flag_chains_badge_and_flag_lookup(self):
        """get_flag delegates to get_badge then badge.get_flag."""
        cert = self._make_cert()
        b = Badge(name="b")
        f = FakeFlag(number=99)
        b.flags.append(f)
        cert.badges.append(b)
        result = cert.get_flag("b", "Test Flag")
        assert result is f
        assert result.number == 99
