"""Tests for advanced flag_1 (AdvancedFlag1)."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.advanced.flag_1 import AdvancedFlag1


class TestAdvancedFlag1:

    def test_name(self):
        f = AdvancedFlag1(number=1)
        assert f.name == 'Adjust sources'

    @pytest.mark.asyncio
    async def test_verify_source_with_facts_and_rules(self):
        f = AdvancedFlag1(number=1)
        source = MagicMock()
        source.facts = [MagicMock()]
        source.rules = [MagicMock()]
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[source])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_no_source(self):
        f = AdvancedFlag1(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_source_no_facts(self):
        f = AdvancedFlag1(number=1)
        source = MagicMock()
        source.facts = []
        source.rules = [MagicMock()]
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[source])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_source_no_rules(self):
        f = AdvancedFlag1(number=1)
        source = MagicMock()
        source.facts = [MagicMock()]
        source.rules = []
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[source])
        assert await f.verify(services) is False
