from app.utility.base_world import BaseWorld


name = 'Kill process on Unauthorized Port'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to kill the previously found ' \
            'process.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_unauth_process_killed(op):
            return True
    return False


def is_unauth_process_killed(op):
    return '02fb7fa9-8886-4330-9e65-fa7bb1bc5271' in [link.ability.ability_id for link in op.chain if link.finish]
