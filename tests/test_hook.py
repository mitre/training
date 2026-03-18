"""Tests for hook.py (plugin enable/expansion/flag loading)."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestHookEnable:
    @pytest.mark.asyncio
    async def test_enable_registers_routes(self):
        from plugins.training.hook import enable
        data_svc = AsyncMock()
        data_svc.apply = AsyncMock()
        data_svc.store = AsyncMock()
        auth_svc = MagicMock()
        app_svc = MagicMock()
        app = MagicMock()
        router = MagicMock()
        app.router = router
        app_svc.application = app

        services = {
            'data_svc': data_svc,
            'auth_svc': auth_svc,
            'app_svc': app_svc,
        }

        with patch('plugins.training.hook.glob.iglob', return_value=[]), \
             patch('plugins.training.hook.TrainingApi'):
            await enable(services)

        data_svc.apply.assert_called_once_with('certifications')
        # Should register routes
        assert router.add_route.call_count > 0
        assert router.add_static.call_count > 0

    @pytest.mark.asyncio
    async def test_enable_adds_correct_routes(self):
        from plugins.training.hook import enable
        data_svc = AsyncMock()
        data_svc.apply = AsyncMock()
        data_svc.store = AsyncMock()
        auth_svc = MagicMock()
        app_svc = MagicMock()
        app = MagicMock()
        router = MagicMock()
        app.router = router
        app_svc.application = app

        services = {
            'data_svc': data_svc,
            'auth_svc': auth_svc,
            'app_svc': app_svc,
        }

        with patch('plugins.training.hook.glob.iglob', return_value=[]), \
             patch('plugins.training.hook.TrainingApi'):
            await enable(services)

        # Check specific routes registered
        route_calls = [str(c) for c in router.add_route.call_args_list]
        route_str = ' '.join(route_calls)
        assert '/plugin/training/gui' in route_str
        assert '/plugin/training/flags' in route_str
        assert '/plugin/training/certs' in route_str
        assert '/plugin/training/reset_flag' in route_str
        assert '/plugin/training/certificate/issue' in route_str
        assert '/plugin/training/certificate/download' in route_str
        assert '/plugin/training/certificate/reset' in route_str


class TestHookExpansion:
    @pytest.mark.asyncio
    async def test_expansion_hides_objects(self):
        from plugins.training.hook import expansion
        data_svc = AsyncMock()
        data_svc.locate = AsyncMock(return_value=[])
        services = {'data_svc': data_svc}

        with patch('plugins.training.hook.glob.iglob', return_value=[]):
            await expansion(services)


class TestHookMetadata:
    def test_name(self):
        from plugins.training.hook import name
        assert name == 'Training'

    def test_description(self):
        from plugins.training.hook import description
        assert 'certification' in description.lower() or 'Caldera' in description

    def test_address(self):
        from plugins.training.hook import address
        assert address == '/plugin/training/gui'


class TestLoadFlags:
    @pytest.mark.asyncio
    async def test_load_flags_no_files(self):
        from plugins.training.hook import _load_flags
        data_svc = AsyncMock()
        with patch('plugins.training.hook.glob.iglob', return_value=[]):
            await _load_flags(data_svc)
        data_svc.store.assert_not_called()


class TestApplyHiddenAccess:
    @pytest.mark.asyncio
    async def test_apply_hidden_no_files(self):
        from plugins.training.hook import _apply_hidden_access_to_loaded_files
        data_svc = AsyncMock()
        with patch('plugins.training.hook.glob.iglob', return_value=[]):
            await _apply_hidden_access_to_loaded_files(data_svc)
        data_svc.locate.assert_not_called()
