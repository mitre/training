from app.utility.base_world import BaseWorld


name = 'Delete New Cron Job'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to delete the previously found ' \
            'cron job.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_file_deleted(op):
            return True
    return False


def is_file_deleted(op):
    return '32e563bb-ba06-4bcc-b817-fc2c434c0b66' in [link.ability.ability_id for link in op.chain if link.finish]
