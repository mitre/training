name = 'Create an adversary'
challenge = 'Create a new adversary named "Certifiable" with at least 3 phases'


async def verify(services):
    check1, check2 = False, False
    for a in await services.get('data_svc').locate('adversaries', dict(name='Certifiable')):
        check1 = len(a.phases) >= 3
    return all([check1, check2])
