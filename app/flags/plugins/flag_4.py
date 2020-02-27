name = 'Mock plugin'
challenge = 'Enable the mock plugin, then run an operation against the simulated group, using the Hunter profile.'


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(adversary_id='de07f52d-9928-4071-9142-cb1d3bd851e8')):
        if op.finish and op.group == 'simulation':
            return True
    return False
