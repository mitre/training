"""Tests for agents blue flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.agents.blue_0 import AgentsBlue0
from plugins.training.app.flags.agents.blue_1 import AgentsBlue1
from plugins.training.app.flags.agents.blue_2 import AgentsBlue2
from plugins.training.app.flags.agents.blue_3 import AgentsBlue3


class TestAgentsBlue0:
    def test_name(self):
        assert AgentsBlue0(number=1).name == 'Red agent - *nix'

    @pytest.mark.asyncio
    async def test_verify_linux_cert_nix(self):
        f = AgentsBlue0(number=1)
        agent = MagicMock(platform='linux', group='cert-nix')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_darwin_cert_nix(self):
        f = AgentsBlue0(number=1)
        agent = MagicMock(platform='darwin', group='cert-nix')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_wrong_platform(self):
        f = AgentsBlue0(number=1)
        agent = MagicMock(platform='windows', group='cert-nix')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_wrong_group(self):
        f = AgentsBlue0(number=1)
        agent = MagicMock(platform='linux', group='red')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False


class TestAgentsBlue1:
    def test_name(self):
        assert AgentsBlue1(number=1).name == 'Blue agent - *nix'

    @pytest.mark.asyncio
    async def test_verify_elevated_blue(self):
        f = AgentsBlue1(number=1)
        agent = MagicMock(platform='linux', group='blue', privilege='Elevated')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_not_elevated(self):
        f = AgentsBlue1(number=1)
        agent = MagicMock(platform='linux', group='blue', privilege='User')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False


class TestAgentsBlue2:
    def test_name(self):
        assert AgentsBlue2(number=1).name == 'Red agent - Windows'

    @pytest.mark.asyncio
    async def test_verify_win_cert_win(self):
        f = AgentsBlue2(number=1)
        agent = MagicMock(platform='windows', group='cert-win')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_linux_fails(self):
        f = AgentsBlue2(number=1)
        agent = MagicMock(platform='linux', group='cert-win')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False


class TestAgentsBlue3:
    def test_name(self):
        assert AgentsBlue3(number=1).name == 'Blue agent - Windows'

    @pytest.mark.asyncio
    async def test_verify_windows_elevated_blue(self):
        f = AgentsBlue3(number=1)
        agent = MagicMock(platform='windows', group='blue', privilege='Elevated')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_not_windows(self):
        f = AgentsBlue3(number=1)
        agent = MagicMock(platform='linux', group='blue', privilege='Elevated')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False
