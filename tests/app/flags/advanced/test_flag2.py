"""Tests for advanced flag_2 (AdvancedFlag2)."""
import pytest
from unittest.mock import MagicMock, patch

from plugins.training.app.flags.advanced.flag_2 import AdvancedFlag2


class TestAdvancedFlag2:

    def test_name(self):
        f = AdvancedFlag2(number=1)
        assert f.name == 'Add new user'

    @pytest.mark.asyncio
    async def test_verify_correct_user(self):
        f = AdvancedFlag2(number=1)
        user = MagicMock()
        user.password = 'hashed-test-password'
        user.permissions = ['red']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        with patch('plugins.training.app.flags.advanced.flag_2.verify_hash', return_value=True) as verify_hash:
            assert await f.verify(services) is True
        verify_hash.assert_called_once_with('hashed-test-password', 'test')

    @pytest.mark.asyncio
    async def test_verify_no_user(self):
        f = AdvancedFlag2(number=1)
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {}
        assert not await f.verify(services)

    @pytest.mark.asyncio
    async def test_verify_wrong_password(self):
        f = AdvancedFlag2(number=1)
        user = MagicMock()
        user.password = 'hashed-wrong-password'
        user.permissions = ['red']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        with patch('plugins.training.app.flags.advanced.flag_2.verify_hash', return_value=False) as verify_hash:
            assert await f.verify(services) is False
        verify_hash.assert_called_once_with('hashed-wrong-password', 'test')

    @pytest.mark.asyncio
    async def test_verify_no_red_permission(self):
        f = AdvancedFlag2(number=1)
        user = MagicMock()
        user.password = 'hashed-test-password'
        user.permissions = ['blue']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        with patch('plugins.training.app.flags.advanced.flag_2.verify_hash', return_value=True) as verify_hash:
            assert await f.verify(services) is False
        verify_hash.assert_called_once_with('hashed-test-password', 'test')
