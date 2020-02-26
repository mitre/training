name = 'Run empty operation'
description = 'Run a new operation, this time not selecting any profiles or groups. Add at least 5 potential links ' \
              'to the operation.'


async def verify(services):
    for op in await services.get('data_svc').locate('abilities', dict(name='operations')):
        if op.finish and not op.adversary and not op.group and len(op.chain) >= 5:
            return True
    return False
