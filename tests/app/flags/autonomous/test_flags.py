"""Tests for autonomous flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.autonomous.blue_0 import AutonomousBlue0
from plugins.training.app.flags.autonomous.blue_1 import AutonomousBlue1
from plugins.training.app.flags.autonomous.blue_3 import AutonomousBlue3


class TestAutonomousBlue0:
    def test_name(self):
        assert AutonomousBlue0(number=1).name == 'Enable Autonomous Operation'

    @pytest.mark.asyncio
    async def test_verify_correct_operation(self):
        f = AutonomousBlue0(number=1)
        adv = MagicMock(adversary_id='7e422753-ad7a-4401-bc8b-b12a28e69c25')
        planner = MagicMock()
        planner.name = 'batch'
        op = MagicMock(adversary=adv, planner=planner)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_wrong_adversary(self):
        f = AutonomousBlue0(number=1)
        adv = MagicMock(adversary_id='wrong-id')
        planner = MagicMock()
        planner.name = 'batch'
        op = MagicMock(adversary=adv, planner=planner)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_wrong_planner(self):
        f = AutonomousBlue0(number=1)
        adv = MagicMock(adversary_id='7e422753-ad7a-4401-bc8b-b12a28e69c25')
        planner = MagicMock()
        planner.name = 'sequential'
        op = MagicMock(adversary=adv, planner=planner)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_operations(self):
        f = AutonomousBlue0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestAutonomousBlue1:
    def test_name(self):
        assert AutonomousBlue1(number=1).name == 'Process on Unauthorized Port'

    @pytest.mark.asyncio
    async def test_verify_detected_and_killed(self):
        f = AutonomousBlue1(number=1)
        op = MagicMock()
        op.ran_ability_id = MagicMock(side_effect=lambda aid: aid in [
            '3b4640bc-eacb-407a-a997-105e39788781',
            '02fb7fa9-8886-4330-9e65-fa7bb1bc5271',
        ])
        fact1 = MagicMock(trait='remote.port.unauthorized')
        fact2 = MagicMock(trait='host.pid.unauthorized')
        op.all_facts = AsyncMock(return_value=[fact1, fact2])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_not_detected(self):
        f = AutonomousBlue1(number=1)
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=False)
        op.all_facts = AsyncMock(return_value=[])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False


class TestAutonomousBlue3:
    def test_name(self):
        assert AutonomousBlue3(number=1).name == 'Suspicious URL in mail'

    @pytest.mark.asyncio
    async def test_verify_url_found_and_inoculated(self):
        f = AutonomousBlue3(number=1)
        fact = MagicMock(trait='remote.suspicious.url')
        op = MagicMock()
        op.all_facts = AsyncMock(return_value=[fact])
        op.ran_ability_id = MagicMock(side_effect=lambda aid: aid in [
            '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce',
            '2ca64acd-dc12-4cc8-b78a-6a182508a50b',
        ])
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_not_inoculated(self):
        f = AutonomousBlue3(number=1)
        fact = MagicMock(trait='remote.suspicious.url')
        op = MagicMock()
        op.all_facts = AsyncMock(return_value=[fact])
        op.ran_ability_id = MagicMock(side_effect=lambda aid: aid == '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_operations(self):
        f = AutonomousBlue3(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False
