from app.utility.base_world import BaseWorld


name = 'Restore Modified PowerShell Profile'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to restore the previously found ' \
            'modified PowerShell Profile with its backup.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_modified_profile_restored(op):
            return True
    return False


def is_modified_profile_restored(op):
    return 'e846973a-767b-4f9c-8b9e-5249cfcd7b97' in [link.ability.ability_id for link in op.chain if link.finish]
