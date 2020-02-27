name = 'Run a basic operation'
challenge = 'Run a new operation, using the Hunter profile and selecting any group of agents'


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(adversary_id='de07f52d-9928-4071-9142-cb1d3bd851e8')):
        if op.finish and len(op.chain) > 5:
            return True
    return False
