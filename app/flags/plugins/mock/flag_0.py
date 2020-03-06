name = 'Mock plugin'
challenge = 'Enable the mock plugin, then run an operation against the simulated group, using the Hunter profile.'
extra_info = """
Testing out attacks ahead of time is the only way to ensure a high chance of success. This can be cumbersome because
you may need a full test lab of varying operating systems to do a full test. Simulating the responses of various TTPs
is a good way to quickly get a feel for how your attack may play out.
"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(group='simulation')):
        if op.finish and op.adversary.adversary_id == 'de07f52d-9928-4071-9142-cb1d3bd851e8':
            return True
    return False
