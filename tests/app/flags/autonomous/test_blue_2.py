from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import yaml

from plugins.training.app.flags.autonomous.blue_2 import AutonomousBlue2

_PLUGIN_ROOT = Path(__file__).resolve().parents[4]


class TestAutonomousBlue2:
    """Tests for the 'Malicious file on system' blue training flag (#167)."""

    def test_flag_importable_from_correct_path(self):
        """The flag class must be importable from flags.autonomous.blue_2."""
        assert AutonomousBlue2 is not None
        assert AutonomousBlue2.name == 'Malicious file on system'

    def test_flag_registered_in_blue_certificate_yaml(self):
        """The flag must be uncommented and listed in the Blue Certificate YAML."""
        yaml_path = _PLUGIN_ROOT / 'data' / 'certifications' / '8da8f0b3-194a-4eed-95b0-43c1f1b64091.yml'
        with open(yaml_path) as f:
            cert = yaml.safe_load(f)
        autonomous_flags = cert['badges']['autonomous']
        assert 'flags.autonomous.blue_2.AutonomousBlue2' in autonomous_flags

    def test_flag_has_no_visible_false(self):
        """The flag should not have visible=False which would hide it from users."""
        assert not hasattr(AutonomousBlue2, 'visible') or AutonomousBlue2.visible is not False

    @pytest.mark.asyncio
    async def test_verify_returns_true_when_file_found_and_deleted(self):
        """Flag should be granted when the file is found AND deleted."""
        flag = AutonomousBlue2(number=1)

        mock_op = MagicMock()
        mock_op.ran_ability_id = MagicMock(return_value=True)

        mock_fact_hash = MagicMock()
        mock_fact_hash.trait = 'file.malicious.hash'
        mock_fact_file = MagicMock()
        mock_fact_file.trait = 'host.malicious.file'
        mock_op.all_facts = AsyncMock(return_value=[mock_fact_hash, mock_fact_file])

        mock_data_svc = AsyncMock()
        mock_data_svc.locate = AsyncMock(return_value=[mock_op])
        services = {'data_svc': mock_data_svc}

        result = await flag.verify(services)
        assert result is True

    @pytest.mark.asyncio
    async def test_verify_returns_false_when_file_not_deleted(self):
        """Flag should NOT be granted when file is found but not deleted."""
        flag = AutonomousBlue2(number=1)

        mock_op = MagicMock()
        # ran_ability_id returns True for find, False for delete
        def selective_ran(ability_id):
            if ability_id == 'f9b3eff0-e11c-48de-9338-1578b351b14b':
                return True  # file found ability
            return False  # file delete ability not run

        mock_op.ran_ability_id = MagicMock(side_effect=selective_ran)

        mock_fact_hash = MagicMock()
        mock_fact_hash.trait = 'file.malicious.hash'
        mock_fact_file = MagicMock()
        mock_fact_file.trait = 'host.malicious.file'
        mock_op.all_facts = AsyncMock(return_value=[mock_fact_hash, mock_fact_file])

        mock_data_svc = AsyncMock()
        mock_data_svc.locate = AsyncMock(return_value=[mock_op])
        services = {'data_svc': mock_data_svc}

        result = await flag.verify(services)
        assert result is False

    @pytest.mark.asyncio
    async def test_verify_returns_false_when_no_operations(self):
        """Flag should NOT be granted when there are no Blue Autonomous operations."""
        flag = AutonomousBlue2(number=1)

        mock_data_svc = AsyncMock()
        mock_data_svc.locate = AsyncMock(return_value=[])
        services = {'data_svc': mock_data_svc}

        result = await flag.verify(services)
        assert result is False
