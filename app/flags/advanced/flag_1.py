name = 'Adjust sources'
challenge = 'Create an entirely new fact source called "better basic" with at least 1 trait and 1 rule'
extra_info = """As an adversary runs TTPs on a host, they look at the output and pick out indicators of interest. These may be
things like user names or passwords, locations of other computers in the network or other useful information. An
adversary makes note of these indicators to use in future TTPs."""


async def verify(services):
    check1, check2 = False, False
    for source in await services.get('data_svc').locate('sources', dict(name='better basic')):
        if len(source.facts) > 0:
            check1 = True
        if len(source.rules) > 0:
            check2 = True
    return all([check1, check2])
