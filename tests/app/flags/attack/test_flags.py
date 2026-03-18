"""Tests for attack blue flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from plugins.training.app.flags.attack.blue_0 import AttackBlue0
from plugins.training.app.flags.attack.blue_1 import AttackBlue1


class TestAttackBlue0:
    def test_name(self):
        assert AttackBlue0(number=1).name == 'ATT&CK Quiz 1'

    @pytest.mark.asyncio
    async def test_verify_delegates_to_base_flag(self):
        f = AttackBlue0(number=1)
        with patch('plugins.training.app.base_flag.BaseFlag.verify_attack_flag',
                    new_callable=AsyncMock, return_value=True) as mock:
            result = await f.verify({'data_svc': AsyncMock(), 'rest_svc': AsyncMock()})
            assert result is True
            mock.assert_called_once()
            args = mock.call_args
            assert args[0][1] == 'T1033'
            assert args[0][2] == 'blue_quiz_1'

    @pytest.mark.asyncio
    async def test_verify_fails(self):
        f = AttackBlue0(number=1)
        with patch('plugins.training.app.base_flag.BaseFlag.verify_attack_flag',
                    new_callable=AsyncMock, return_value=False):
            result = await f.verify({'data_svc': AsyncMock(), 'rest_svc': AsyncMock()})
            assert result is False


class TestAttackBlue1:
    def test_name(self):
        assert AttackBlue1(number=1).name == 'ATT&CK Quiz 2'

    @pytest.mark.asyncio
    async def test_verify_technique(self):
        f = AttackBlue1(number=1)
        with patch('plugins.training.app.base_flag.BaseFlag.verify_attack_flag',
                    new_callable=AsyncMock, return_value=True) as mock:
            result = await f.verify({'data_svc': AsyncMock(), 'rest_svc': AsyncMock()})
            assert result is True
            args = mock.call_args
            assert args[0][1] == 'T1083'
            assert args[0][2] == 'blue_quiz_2'
