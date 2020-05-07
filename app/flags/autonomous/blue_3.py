from app.utility.base_world import BaseWorld


name = 'Suspicious URL in mail'
challenge = 'Use the \'mail\' utility to send an email to a user on the Linux or Darwin machine. Spoof the sender ' \
            'address to be an email address with a fake malicious domain. The autonomous defender should find this ' \
            'URL and add an entry to the /etc/hosts file, redirecting the URL to localhost.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Autonomous')):
        if is_url_found(op) and is_url_inoculated(op):
            return True
    return False


def is_url_found(op):
    if 'remote.suspicious.url' in [f.trait for f in op.all_facts()] and \
            '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce' in [link.ability.ability_id for link in op.chain]:
        return True
    return False


def is_url_inoculated(op):
    return '2ca64acd-dc12-4cc8-b78a-6a182508a50b' in [link.ability.ability_id for link in op.chain if link.finish]
