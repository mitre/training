name = 'Adjust sources'
challenge = 'Add a new trait "training" with any value and a new rule to the basic fact source. ' \
            'Then create an entirely new fact source called "better_basic" with at least 1 trait.'
extra_info = """
As an adversary runs TTPs on a host, they look at the output and pick out indicators of interest. These may be 
things like user names or passwords, locations of other computers in the network or other useful information. An 
adversary makes note of these indicators to use in future TTPs.
"""


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
