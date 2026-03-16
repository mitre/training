"""Tests for manual blue flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from plugins.training.app.flags.manual.blue_0 import ManualBlue0
from plugins.training.app.flags.manual.blue_1a import ManualBlue1a


class TestManualBlue0:
    def test_name(self):
        assert ManualBlue0(number=1).name == 'Enable Manual Operation'

    @pytest.mark.asyncio
    async def test_verify_adhoc_blue_manual(self):
        f = ManualBlue0(number=1)
        adv = MagicMock(adversary_id='ad-hoc')
        op = MagicMock(adversary=adv)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_wrong_adversary(self):
        f = ManualBlue0(number=1)
        adv = MagicMock(adversary_id='not-adhoc')
        op = MagicMock(adversary=adv)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_op(self):
        f = ManualBlue0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestManualBlue1a:
    def test_name(self):
        assert ManualBlue1a(number=1).name == 'Detect process on Unauthorized Port'

    def test_additional_fields(self):
        f = ManualBlue1a(number=1)
        assert f.additional_fields['operation_name'] == 'training_manual_1'
        assert f.additional_fields['adversary_id'] == '72c0b333-f6fe-4fa0-a342-4215e8de3947'
        assert f.additional_fields['agent_group'] == 'cert-nix'

    def test_is_resettable(self):
        f = ManualBlue1a(number=1)
        assert f._is_resettable() == 'True'

    @pytest.mark.asyncio
    async def test_verify_delegates_to_standard_verify(self):
        f = ManualBlue1a(number=1)
        with patch('plugins.training.app.base_flag.BaseFlag.standard_verify_with_operation',
                    new_callable=AsyncMock, return_value=True):
            result = await f.verify({'data_svc': AsyncMock()})
            assert result is True
