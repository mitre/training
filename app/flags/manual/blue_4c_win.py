from app.utility.base_world import BaseWorld


name = 'Delete New Scheduled Task'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to delete the previously found ' \
            'scheduled task.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_file_deleted(op):
            return True
    return False


def is_file_deleted(op):
    return '4744d99f-5fea-42a8-8ec4-c228db57caea' in [link.ability.ability_id for link in op.chain if link.finish]
