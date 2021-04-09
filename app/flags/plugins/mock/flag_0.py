from plugins.training.app.c_flag import Flag


class PluginsMockFlag0(Flag):
    name = 'Mock plugin'
    challenge = (
        'Enable the mock plugin. Then run an operation against the "simulation" group using the Hunter profile. '
        '(Hint: check default.yml for running plugins.)'
    )
    extra_info = (
        'Testing out attacks ahead of time ensures a high chance of success during a real operation. This can be '
        'cumbersome if the test requires a test lab with varying operating systems. Simulating the responses of '
        'various TTPs is a good way to quickly get a feel for how an attack may play out.'
    )

    async def verify(self, services):
        if await services.get('data_svc').locate('plugins', dict(name='mock', enabled=True)):
            for op in await services.get('data_svc').locate('operations', dict(group='simulation')):
                if op.finish and op.adversary.adversary_id == 'de07f52d-9928-4071-9142-cb1d3bd851e8':
                    return True
        return False
