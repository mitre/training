"""Tests for plugin flag modules (compass, manx, response)."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.plugins.compass.flag_0 import PluginsCompassFlag0
from plugins.training.app.flags.plugins.manx.flag_0 import PluginsManxFlag0
from plugins.training.app.flags.plugins.manx.flag_1 import PluginsManxFlag1
from plugins.training.app.flags.plugins.response.flag_0 import PluginsResponseFlag0
from plugins.training.app.flags.plugins.response.flag_1 import PluginsResponseFlag1


class TestPluginsCompassFlag0:
    def test_name(self):
        assert PluginsCompassFlag0(number=1).name == 'Compass plugin'

    @pytest.mark.asyncio
    async def test_verify_compass_adversary(self):
        f = PluginsCompassFlag0(number=1)
        adv = MagicMock(description='created in compass')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_compass(self):
        f = PluginsCompassFlag0(number=1)
        adv = MagicMock(description='not from plugin')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[adv])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_adversaries(self):
        f = PluginsCompassFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestPluginsManxFlag0:
    def test_name(self):
        assert PluginsManxFlag0(number=1).name == 'Manx plugin'

    @pytest.mark.asyncio
    async def test_verify_no_tcp_agents(self):
        f = PluginsManxFlag0(number=1)
        services = {
            'data_svc': AsyncMock(),
            'contact_svc': MagicMock(report={'websocket': []}),
        }
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestPluginsManxFlag1:
    def test_name(self):
        assert PluginsManxFlag1(number=1).name == 'Manx UDP'

    @pytest.mark.asyncio
    async def test_verify_udp_agent(self):
        f = PluginsManxFlag1(number=1)
        agent = MagicMock(contact='udp')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_udp(self):
        f = PluginsManxFlag1(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestPluginsResponseFlag0:
    def test_name(self):
        assert PluginsResponseFlag0(number=1).name == 'Blue agent'

    @pytest.mark.asyncio
    async def test_verify_blue_agent(self):
        f = PluginsResponseFlag0(number=1)
        agent = MagicMock(group='blue')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_blue(self):
        f = PluginsResponseFlag0(number=1)
        agent = MagicMock(group='red')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_agents(self):
        f = PluginsResponseFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestPluginsResponseFlag1:
    def test_name(self):
        assert PluginsResponseFlag1(number=1).name == 'Blue operation'

    @pytest.mark.asyncio
    async def test_verify_correct_blue_op(self):
        f = PluginsResponseFlag1(number=1)
        adv = MagicMock(adversary_id='7e422753-ad7a-4401-bc8b-b12a28e69c25')
        op = MagicMock(agents=[MagicMock()], group='blue', adversary=adv)
        op.ran_ability_id = MagicMock(return_value=True)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_ops(self):
        f = PluginsResponseFlag1(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False
