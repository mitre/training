"""Tests for agents flag modules."""
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from plugins.training.app.flags.agents.flag_0 import AgentsFlag0
from plugins.training.app.flags.agents.flag_1 import AgentsFlag1
from plugins.training.app.flags.agents.flag_2 import AgentsFlag2
from plugins.training.app.flags.agents.flag_3 import AgentsFlag3
from plugins.training.app.flags.agents.flag_4 import AgentsFlag4
from plugins.training.app.flags.agents.flag_5 import AgentsFlag5
from plugins.training.app.flags.agents.flag_6 import AgentsFlag6
from plugins.training.app.flags.agents.flag_7 import AgentsFlag7


class TestAgentsFlag0:
    def test_name(self):
        assert AgentsFlag0(number=1).name == 'Local agent'

    @pytest.mark.asyncio
    async def test_verify_agent_exists(self):
        f = AgentsFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[MagicMock()])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_agents(self):
        f = AgentsFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestAgentsFlag1:
    def test_name(self):
        assert AgentsFlag1(number=1).name == 'Remote agent'

    @pytest.mark.asyncio
    async def test_verify_remote_agent(self):
        f = AgentsFlag1(number=1)
        local_agent = MagicMock(platform=sys.platform, server='10.0.0.1')
        remote_agent = MagicMock(platform='different_platform', server='10.0.0.2')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[local_agent, remote_agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_single_agent(self):
        f = AgentsFlag1(number=1)
        agent = MagicMock(platform=sys.platform, server='10.0.0.1')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_same_platform(self):
        f = AgentsFlag1(number=1)
        a1 = MagicMock(platform=sys.platform, server='10.0.0.1')
        a2 = MagicMock(platform=sys.platform, server='10.0.0.2')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[a1, a2])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_localhost_server(self):
        f = AgentsFlag1(number=1)
        a1 = MagicMock(platform=sys.platform, server='127.0.0.1')
        a2 = MagicMock(platform='other', server='localhost')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[a1, a2])
        assert await f.verify(services) is False


class TestAgentsFlag2:
    def test_name(self):
        assert AgentsFlag2(number=1).name == 'Understanding trust'

    @pytest.mark.asyncio
    async def test_verify_correct_timer(self):
        f = AgentsFlag2(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(lambda name=None, prop=None: 60 if prop == 'untrusted_timer' else None)
        try:
            assert await f.verify({}) is True
        finally:
            BaseWorld.get_config = original

    @pytest.mark.asyncio
    async def test_verify_wrong_timer(self):
        f = AgentsFlag2(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(lambda name=None, prop=None: 30)
        try:
            assert await f.verify({}) is False
        finally:
            BaseWorld.get_config = original


class TestAgentsFlag3:
    def test_name(self):
        assert AgentsFlag3(number=1).name == 'Update agent'

    @pytest.mark.asyncio
    async def test_verify_modified_agent(self):
        f = AgentsFlag3(number=1)
        agent = MagicMock(group='custom', sleep_min=10, sleep_max=20)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_default_agent(self):
        f = AgentsFlag3(number=1)
        agent = MagicMock(group='red', sleep_min=30, sleep_max=60)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False


class TestAgentsFlag4:
    def test_name(self):
        assert AgentsFlag4(number=1).name == 'Agent filename'

    @pytest.mark.asyncio
    async def test_verify_correct_name(self):
        f = AgentsFlag4(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(lambda name=None, prop=None: 'super_scary' if prop == 'implant_name' else None)
        try:
            assert await f.verify({}) is True
        finally:
            BaseWorld.get_config = original

    @pytest.mark.asyncio
    async def test_verify_wrong_name(self):
        f = AgentsFlag4(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(lambda name=None, prop=None: 'sandcat')
        try:
            assert await f.verify({}) is False
        finally:
            BaseWorld.get_config = original


class TestAgentsFlag5:
    def test_name(self):
        assert AgentsFlag5(number=1).name == 'Bootstrap abilities'

    @pytest.mark.asyncio
    async def test_verify_correct_bootstrap(self):
        f = AgentsFlag5(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(
            lambda name=None, prop=None: ['c0da588f-79f0-4263-8998-7496b1a40596'] if prop == 'bootstrap_abilities' else None
        )
        try:
            assert await f.verify({}) is True
        finally:
            BaseWorld.get_config = original

    @pytest.mark.asyncio
    async def test_verify_missing_bootstrap(self):
        f = AgentsFlag5(number=1)
        from app.utility.base_world import BaseWorld
        original = BaseWorld.get_config
        BaseWorld.get_config = staticmethod(lambda name=None, prop=None: [])
        try:
            assert await f.verify({}) is False
        finally:
            BaseWorld.get_config = original


class TestAgentsFlag6:
    def test_name(self):
        assert AgentsFlag6(number=1).name == 'Contact points'

    @pytest.mark.asyncio
    async def test_verify_multiple_contacts(self):
        f = AgentsFlag6(number=1)
        a1 = MagicMock(contact='http')
        a2 = MagicMock(contact='tcp')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[a1, a2])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_single_contact(self):
        f = AgentsFlag6(number=1)
        a1 = MagicMock(contact='http')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[a1])
        assert await f.verify(services) is False


class TestAgentsFlag7:
    def test_name(self):
        assert AgentsFlag7(number=1).name == 'Kill agent'

    @pytest.mark.asyncio
    async def test_verify_watchdog_set(self):
        f = AgentsFlag7(number=1)
        agent = MagicMock(watchdog=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_watchdog(self):
        f = AgentsFlag7(number=1)
        agent = MagicMock(watchdog=0)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[agent])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_agents(self):
        f = AgentsFlag7(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False
