"""Tests for adversaries flags."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.adversaries.flag_0 import AdversariesFlag0
from plugins.training.app.flags.adversaries.flag_1 import AdversariesFlag1
from plugins.training.app.flags.adversaries.flag_2 import AdversariesFlag2


class TestAdversariesFlag0:
    def test_name(self):
        assert AdversariesFlag0(number=1).name == 'Create adversary'

    @pytest.mark.asyncio
    async def test_verify_enough_abilities(self):
        f = AdversariesFlag0(number=1)
        adv = MagicMock()
        adv.atomic_ordering = ['a1', 'a2', 'a3']
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_too_few_abilities(self):
        f = AdversariesFlag0(number=1)
        adv = MagicMock()
        adv.atomic_ordering = ['a1']
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_adversary(self):
        f = AdversariesFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_exactly_three(self):
        f = AdversariesFlag0(number=1)
        adv = MagicMock()
        adv.atomic_ordering = ['a1', 'a2', 'a3']
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is True


class TestAdversariesFlag1:
    def test_name(self):
        assert AdversariesFlag1(number=1).name == 'Combine adversaries'

    @pytest.mark.asyncio
    async def test_verify_has_nosy_neighbor(self):
        f = AdversariesFlag1(number=1)
        adv = MagicMock()
        adv.atomic_ordering = ['other', '2fe2d5e6-7b06-4fc0-bf71-6966a1226731']
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_missing_nosy(self):
        f = AdversariesFlag1(number=1)
        adv = MagicMock()
        adv.atomic_ordering = ['other']
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_adversary(self):
        f = AdversariesFlag1(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestAdversariesFlag2:
    def test_name(self):
        assert AdversariesFlag2(number=1).name == 'Create ability'

    @pytest.mark.asyncio
    async def test_verify_correct_ability(self):
        f = AdversariesFlag2(number=1)
        executor = MagicMock()
        executor.cleanup = 'rm -f /tmp/test'
        executor.command = 'ifconfig'
        ability = MagicMock()
        ability.tactic = 'discovery'
        ability.executors = [executor]
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[ability])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_wrong_tactic(self):
        f = AdversariesFlag2(number=1)
        executor = MagicMock()
        executor.cleanup = 'cmd'
        executor.command = 'cmd'
        ability = MagicMock()
        ability.tactic = 'persistence'
        ability.executors = [executor]
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[ability])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_cleanup(self):
        f = AdversariesFlag2(number=1)
        executor = MagicMock()
        executor.cleanup = ''
        executor.command = 'ifconfig'
        ability = MagicMock()
        ability.tactic = 'discovery'
        ability.executors = [executor]
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[ability])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_ability(self):
        f = AdversariesFlag2(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False
