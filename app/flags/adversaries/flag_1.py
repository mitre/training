name = 'Add a pack'
challenge = 'Add the Nosy Neighbor adversary pack to the Certifiable adversary and save it'
extra_info = """A TTP is often connected to a series of other TTPs to form an attack. For example, an adversary may have a procedure
for locating all PDF files on a host. This may be followed by a procedure to exfiltrate all the found files. In
CALDERA, this chain of TTPs being used is considered a pack."""


async def verify(services):
    for a in await services.get('data_svc').locate('adversaries', dict(name='Certifiable')):
        for _, abilities in a.phases.items():
            for ability in abilities:
                if ability.ability_id == '2fe2d5e6-7b06-4fc0-bf71-6966a1226731':
                    return True
    return False
