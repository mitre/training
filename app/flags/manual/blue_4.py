from app.utility.base_world import BaseWorld


name = 'Hunt for malicious file on system'
challenge = 'Run the appropriate hunt ability in the \'Blue Manual\' operation to find the location of the ' \
            'malicious file.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_file_found(op):
            return True
    return False


def is_file_found(op):
    return 'host.malicious.file' in [f.trait for f in op.all_facts()] and \
            'f9b3eff0-e11c-48de-9338-1578b351b14b' in [link.ability.ability_id for link in op.chain if link.finish]
