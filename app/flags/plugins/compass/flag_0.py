name = 'Compass plugin'
challenge = 'In the Compass plugin, create a new adversary'


async def verify(services):
    for a in await services.get('data_svc').locate('adversaries'):
        if 'compass' in a.description:
            return True
    return False
