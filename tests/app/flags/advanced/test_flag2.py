"""Tests for advanced flag_2 (AdvancedFlag2)."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.advanced.flag_2 import AdvancedFlag2


class TestAdvancedFlag2:

    def test_name(self):
        f = AdvancedFlag2(number=1)
        assert f.name == 'Add new user'

    @pytest.mark.asyncio
    async def test_verify_correct_user(self):
        f = AdvancedFlag2(number=1)
        user = MagicMock()
        user.password = 'test'
        user.permissions = ['red']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        assert await f.verify(services) is True

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
        user.password = 'wrong'
        user.permissions = ['red']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_red_permission(self):
        f = AdvancedFlag2(number=1)
        user = MagicMock()
        user.password = 'test'
        user.permissions = ['blue']
        services = {'auth_svc': MagicMock()}
        services['auth_svc'].user_map = {'test': user}
        assert await f.verify(services) is False
