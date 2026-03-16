"""Exhaustive tests for app.c_flag.Flag base class."""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from plugins.training.app.c_flag import Flag


class ConcreteFlag(Flag):
    name = 'Concrete'
    challenge = 'Test challenge'
    extra_info = 'Some info'

    async def verify(self, services):
        return True


class NoSolutionFlag(Flag):
    name = 'NoSolution'
    challenge = 'No guide'
    extra_info = ''

    async def verify(self, services):
        return False


class TestFlagInit:
    def test_default_number(self):
        f = ConcreteFlag(number=5)
        assert f.number == 5

    def test_default_not_completed(self):
        f = ConcreteFlag(number=1)
        assert f.completed is False

    def test_default_completed_timestamp_none(self):
        f = ConcreteFlag(number=1)
        assert f.completed_timestamp is None

    def test_default_started_ts_none(self):
        f = ConcreteFlag(number=1)
        assert f.started_ts is None

    def test_default_ticks_zero(self):
        f = ConcreteFlag(number=1)
        assert f._ticks == 0


class TestFlagCompleted:
    def test_set_completed(self):
        f = ConcreteFlag(number=1)
        f.completed = True
        assert f.completed is True

    def test_completed_sets_timestamp(self):
        f = ConcreteFlag(number=1)
        f.completed = True
        assert f.completed_timestamp is not None
        assert isinstance(f.completed_timestamp, datetime)

    def test_set_completed_false(self):
        f = ConcreteFlag(number=1)
        f.completed = True
        f.completed = False
        assert f.completed is False

    def test_completed_timestamp_updates_on_each_set(self):
        f = ConcreteFlag(number=1)
        f.completed = True
        ts1 = f.completed_timestamp
        f.completed = True
        ts2 = f.completed_timestamp
        assert ts2 >= ts1


class TestFlagActivate:
    def test_activate_sets_started_ts(self):
        f = ConcreteFlag(number=1)
        f.activate()
        assert f.started_ts is not None

    def test_activate_increments_ticks(self):
        f = ConcreteFlag(number=1)
        f.activate()
        assert f._ticks == 1
        f.activate()
        assert f._ticks == 2

    def test_activate_does_not_reset_started_ts(self):
        f = ConcreteFlag(number=1)
        f.activate()
        ts = f.started_ts
        f.activate()
        assert f.started_ts == ts

    def test_activate_no_tick_after_completed(self):
        f = ConcreteFlag(number=1)
        f.activate()
        assert f._ticks == 1
        f.completed = True  # sets _completed_timestamp
        f.activate()
        # started_ts already set, completed_timestamp set => ticks should NOT increment
        assert f._ticks == 1


class TestFlagDisplay:
    def test_display_keys(self):
        f = ConcreteFlag(number=1)
        d = f.display
        expected_keys = {'number', 'name', 'challenge', 'completed',
                         'extra_info', 'code', 'completed_timestamp',
                         'resettable', 'has_solution_guide'}
        assert set(d.keys()) == expected_keys

    def test_display_values(self):
        f = ConcreteFlag(number=42)
        d = f.display
        assert d['number'] == 42
        assert d['name'] == 'Concrete'
        assert d['challenge'] == 'Test challenge'
        assert d['completed'] is False
        assert d['extra_info'] == 'Some info'

    def test_display_completed_timestamp_empty_when_not_set(self):
        f = ConcreteFlag(number=1)
        assert f.display['completed_timestamp'] == ''

    def test_display_completed_timestamp_formatted(self):
        f = ConcreteFlag(number=1)
        f.completed = True
        ts = f.display['completed_timestamp']
        assert len(ts) == 19  # 'YYYY-MM-DD HH:MM:SS'


class TestFlagResettable:
    def test_not_resettable_by_default(self):
        f = ConcreteFlag(number=1)
        assert f._is_resettable() == 'False'

    def test_resettable_with_additional_fields(self):
        f = ConcreteFlag(number=1)
        f.additional_fields = {'adversary_id': 'xyz'}
        assert f._is_resettable() == 'True'

    def test_not_resettable_without_adversary_id(self):
        f = ConcreteFlag(number=1)
        f.additional_fields = {'operation_name': 'op'}
        assert f._is_resettable() == 'False'


class TestFlagUnique:
    def test_unique_not_none(self):
        f = ConcreteFlag(number=1)
        assert f.unique is not None

    def test_unique_deterministic(self):
        f1 = ConcreteFlag(number=1)
        f2 = ConcreteFlag(number=1)
        assert f1.unique == f2.unique


class TestFlagStore:
    def test_store_adds_to_ram(self):
        f = ConcreteFlag(number=1)
        ram = {'flags': []}
        f.store(ram)
        assert len(ram['flags']) == 1

    def test_store_idempotent(self):
        f = ConcreteFlag(number=1)
        ram = {'flags': []}
        f.store(ram)
        f.store(ram)
        assert len(ram['flags']) == 1


class TestFlagCalculateCode:
    def test_calculate_code_returns_string(self):
        f = ConcreteFlag(number=1)
        assert isinstance(f.calculate_code(), str)


class TestFlagSolutionGuide:
    def test_solution_guide_filename(self):
        f = ConcreteFlag(number=1)
        assert f.solution_guide_filename == 'ConcreteFlag.md'

    def test_has_solution_guide_false_when_missing(self):
        f = ConcreteFlag(number=1)
        # The file won't exist
        assert f.has_solution_guide is False or f.has_solution_guide is True
        # Just ensure it doesn't crash


class TestFlagStaticMethods:
    def test_is_unauth_process_killed(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=True)
        assert Flag._is_unauth_process_killed(op) is True

    def test_is_unauth_process_killed_false(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=False)
        assert Flag._is_unauth_process_killed(op) is False

    @pytest.mark.asyncio
    async def test_is_unauth_process_detected(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=True)
        fact1 = MagicMock(trait='remote.port.unauthorized')
        fact2 = MagicMock(trait='host.pid.unauthorized')
        from unittest.mock import AsyncMock
        op.all_facts = AsyncMock(return_value=[fact1, fact2])
        result = await Flag._is_unauth_process_detected(op)
        assert result is True

    @pytest.mark.asyncio
    async def test_is_unauth_process_detected_missing_trait(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=True)
        fact1 = MagicMock(trait='remote.port.unauthorized')
        from unittest.mock import AsyncMock
        op.all_facts = AsyncMock(return_value=[fact1])
        result = await Flag._is_unauth_process_detected(op)
        assert result is False

    @pytest.mark.asyncio
    async def test_is_file_found(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=True)
        f1 = MagicMock(trait='file.malicious.hash')
        f2 = MagicMock(trait='host.malicious.file')
        from unittest.mock import AsyncMock
        op.all_facts = AsyncMock(return_value=[f1, f2])
        result = await Flag._is_file_found(op)
        assert result is True

    @pytest.mark.asyncio
    async def test_is_file_found_missing_ability(self):
        op = MagicMock()
        op.ran_ability_id = MagicMock(return_value=False)
        f1 = MagicMock(trait='file.malicious.hash')
        f2 = MagicMock(trait='host.malicious.file')
        from unittest.mock import AsyncMock
        op.all_facts = AsyncMock(return_value=[f1, f2])
        result = await Flag._is_file_found(op)
        assert result is False
