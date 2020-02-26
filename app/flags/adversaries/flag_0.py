name = 'Create an adversary'
challenge = 'Create a new adversary named "Certifiable" with at least 3 phases'


async def verify(services):
    for a in await services.get('data_svc').locate('adversaries', dict(name='Certifiable')):
        return len(a.phases) >= 3
    return False
