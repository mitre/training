"""Tests for developers flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from plugins.training.app.flags.developers.flag_0 import DevelopersFlag0
from plugins.training.app.flags.developers.flag_2 import DevelopersFlag2
from plugins.training.app.flags.developers.flag_6 import DevelopersFlag6
from plugins.training.app.flags.developers.flag_7 import DevelopersFlag7


class TestDevelopersFlag0:
    def test_name(self):
        assert DevelopersFlag0(number=1).name == 'Create a new plugin'

    @pytest.mark.asyncio
    async def test_verify_no_plugin(self):
        f = DevelopersFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestDevelopersFlag2:
    def test_name(self):
        assert DevelopersFlag2(number=1).name == 'Bypass authentication'

    @pytest.mark.asyncio
    async def test_verify_bypass_set(self):
        f = DevelopersFlag2(number=1)
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].bypass = ['127.0.0.1']
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_bypass_not_set(self):
        f = DevelopersFlag2(number=1)
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].bypass = []
        assert await f.verify(services) is False


class TestDevelopersFlag6:
    def test_name(self):
        assert DevelopersFlag6(number=1).name == 'Build an agent'

    @pytest.mark.asyncio
    async def test_verify_zsh_agent(self):
        f = DevelopersFlag6(number=1)
        agent = MagicMock(executors=['zsh'])
        op = MagicMock(chain=[MagicMock()], agents=[agent])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_zsh(self):
        f = DevelopersFlag6(number=1)
        agent = MagicMock(executors=['sh'])
        op = MagicMock(chain=[MagicMock()], agents=[agent])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_empty_chain(self):
        f = DevelopersFlag6(number=1)
        op = MagicMock(chain=[], agents=[])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False


class TestDevelopersFlag7:
    def test_name(self):
        assert DevelopersFlag7(number=1).name == 'Understanding access'

    @pytest.mark.asyncio
    async def test_verify_blue_access(self):
        f = DevelopersFlag7(number=1)
        from app.utility.base_world import BaseWorld
        plugin = MagicMock(access=BaseWorld.Access.BLUE)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[plugin])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_red_access(self):
        f = DevelopersFlag7(number=1)
        from app.utility.base_world import BaseWorld
        plugin = MagicMock(access=BaseWorld.Access.RED)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[plugin])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_plugin(self):
        f = DevelopersFlag7(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False
