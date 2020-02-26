name = 'Create an ability'
description = 'Create a new ability named "My test ability". Put it under the discovery tactic and include a payload ' \
              'and a cleanup command.'


async def verify(services):
    check1, check2, check3 = False, False, False
    for a in await services.get('data_svc').locate('abilities', dict(name='My test ability')):
        check1 = a.tactic == 'discovery'
        check2 = a.payload is not None
        check3 = a.cleanup is not None
    return all([check1, check2, check3])
