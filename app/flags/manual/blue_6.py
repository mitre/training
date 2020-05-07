from app.utility.base_world import BaseWorld


name = 'Find suspicious URL in mail'
challenge = 'Use the \'mail\' utility to send an email to a user on the Linux or Darwin machine. Spoof the sender ' \
            'address to be an email address with a fake malicious domain. Run the appropriate detection ' \
            'ability in the \'Blue Manual\' operation to find this URL.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_url_found(op):
            return True
    return False


def is_url_found(op):
    return 'remote.suspicious.url' in [f.trait for f in op.all_facts()] and \
            '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce' in [link.ability.ability_id for link in op.chain if link.finish]
