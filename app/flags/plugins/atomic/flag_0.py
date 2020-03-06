name = 'Atomic plugin'
challenge = 'Enable the Atomic plugin and verify that new abilities have been added to the database'


async def verify(services):
    for _ in await services.get('data_svc').locate('plugins', dict(enabled=True, name='atomic')):
        return True
    return False
