from plugins.training.app.c_flag import Flag


class OperationsFlag0(Flag):
    name = 'Basic operation'
    challenge = 'Run and finish an operation. Use the Hunter adversary profile provided in the Stockpile plugin.'
    extra_info = (
        'An autonomous operation uses an adversary profile to pre-configures the attack. Agents and C2 run '
        'without operator interference. This allows operators to run repeatable adversary emulation '
        'exercises, ensuring that each one is identical to the last.'
    )

    async def verify(self, services):
        for op in await services.get('data_svc').locate('operations'):
            if op.finish and op.adversary.adversary_id == 'de07f52d-9928-4071-9142-cb1d3bd851e8':
                return True
        return False
