"""Tests for operations flag modules."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.operations.flag_0 import OperationsFlag0
from plugins.training.app.flags.operations.flag_1 import OperationsFlag1
from plugins.training.app.flags.operations.flag_2 import OperationsFlag2
from plugins.training.app.flags.operations.flag_3 import OperationsFlag3


class TestOperationsFlag0:
    def test_name(self):
        assert OperationsFlag0(number=1).name == 'Basic operation'

    @pytest.mark.asyncio
    async def test_verify_finished_check(self):
        f = OperationsFlag0(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish='2023-01-01', adversary=adv)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_not_finished(self):
        f = OperationsFlag0(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish=None, adversary=adv)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_wrong_adversary(self):
        f = OperationsFlag0(number=1)
        adv = MagicMock(adversary_id='wrong')
        op = MagicMock(finish='done', adversary=adv)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_no_ops(self):
        f = OperationsFlag0(number=1)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[])
        assert await f.verify(services) is False


class TestOperationsFlag1:
    def test_name(self):
        assert OperationsFlag1(number=1).name == 'Stealthy operation'

    @pytest.mark.asyncio
    async def test_verify_stealthy(self):
        f = OperationsFlag1(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish='done', adversary=adv, obfuscator='base64', jitter='10/20')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_wrong_obfuscator(self):
        f = OperationsFlag1(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish='done', adversary=adv, obfuscator='plain', jitter='10/20')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_wrong_jitter(self):
        f = OperationsFlag1(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish='done', adversary=adv, obfuscator='base64', jitter='5/10')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False


class TestOperationsFlag2:
    def test_name(self):
        assert OperationsFlag2(number=1).name == 'Manual operation'

    @pytest.mark.asyncio
    async def test_verify_manual(self):
        f = OperationsFlag2(number=1)
        adv = MagicMock(adversary_id='different')
        op = MagicMock(finish='done', adversary=adv, autonomous=False)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_autonomous_fails(self):
        f = OperationsFlag2(number=1)
        adv = MagicMock(adversary_id='different')
        op = MagicMock(finish='done', adversary=adv, autonomous=True)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_check_adversary_fails(self):
        f = OperationsFlag2(number=1)
        adv = MagicMock(adversary_id='01d77744-2515-401a-a497-d9f7241aac3c')
        op = MagicMock(finish='done', adversary=adv, autonomous=False)
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False


class TestOperationsFlag3:
    def test_name(self):
        assert OperationsFlag3(number=1).name == 'Empty operation'

    @pytest.mark.asyncio
    async def test_verify_empty_op(self):
        f = OperationsFlag3(number=1)
        adv = MagicMock(adversary_id='ad-hoc')
        op = MagicMock(finish='done', adversary=adv, chain=[1, 2, 3, 4, 5], group='')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is True

    @pytest.mark.asyncio
    async def test_verify_too_few_links(self):
        f = OperationsFlag3(number=1)
        adv = MagicMock(adversary_id='ad-hoc')
        op = MagicMock(finish='done', adversary=adv, chain=[1, 2], group='')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False

    @pytest.mark.asyncio
    async def test_verify_has_group_fails(self):
        f = OperationsFlag3(number=1)
        adv = MagicMock(adversary_id='ad-hoc')
        op = MagicMock(finish='done', adversary=adv, chain=[1, 2, 3, 4, 5], group='red')
        services = {'data_svc': AsyncMock()}
        services['data_svc'].locate = AsyncMock(return_value=[op])
        assert await f.verify(services) is False
