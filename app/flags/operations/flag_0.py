name = 'Basic operation'
challenge = 'Run a new operation, using the Hunter profile and select any group of agents'
extra_info = """An autonomous operation is where an adversary pre-configures their attack and let's their agent and C2 operate
without their interference. From a red-team perspective, this is an invaluable way to run repeatable adversary
emulation exercises, ensuring that each one is identical to the last."""


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and op.adversary.adversary_id == 'de07f52d-9928-4071-9142-cb1d3bd851e8':
            return True
    return False
