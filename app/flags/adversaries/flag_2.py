name = 'Create ability'
challenge = 'Create a new ability from the UI named "My test ability" and add it to the Certifiable adversary. Put ' \
            'it under the discovery tactic and include a command to execute and a cleanup command. Have the command ' \
            'print out the network interfaces and IP addresses on the host. Hint: this would be "ifconfig" on a MacOS.'
extra_info = """Being able to create TTPs quickly and swap them in and out is a valuable skill. Adversaries use a
 TTP until it is no longer effective - and then they write new versions, make modifications or switch techniques
 entirely."""


async def verify(services):
    check1, check2, check3 = False, False, False
    for a in await services.get('data_svc').locate('abilities', dict(name='My test ability')):
        check1 = a.tactic == 'discovery'
        check2 = a.payloads is not None
        check3 = a.cleanup is not None
    return all([check1, check2, check3])
