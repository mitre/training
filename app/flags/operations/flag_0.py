name = 'Run a basic operation'
description = 'Run a new operation, using the Hunter profile and selecting any group of agents'


async def verify(services):
    for op in await services.get('data_svc').locate('abilities', dict(name='operations')):
        if op.finish and len(op.chain) > 10:
            return True
    return False
