name = 'Adjust sources'
challenge = 'Add a new trait "training" with any value and a new rule to the basic fact source. ' \
            'Then create an entirely new fact source called "better_basic" with at least 1 trait.'


async def verify(services):
    check1, check2, check3 = False, False, False
    source = await services.get('data_svc').locate('sources', dict(name='basic'))
    for fact in source[0].facts:
        if fact.trait == 'training':
            check1 = True
    if len(source[0].rules) > 4:
        check2 = True
    for _ in await services.get('data_svc').locate('sources', dict(name='better_basic')):
        check3 = True
    return all([check1, check2, check3])
