from app.utility.base_world import BaseWorld


name = 'Backup PowerShell Profiles'
challenge = 'Run the appropriate setup ability in the \'Blue Manual\' operation to backup all the PowerShell ' \
            'Profiles on the Windows machine.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if powershell_profiles_backed_up(op):
            return True
    return False


def powershell_profiles_backed_up(op):
    return '83d7cf63-e10a-4615-a92e-dce257bf3b9d' in [link.ability.ability_id for link in op.chain if link.finish]
