from app.utility.base_world import BaseWorld


name = 'Acquire PowerShell Profile Hashes'
challenge = 'Run the appropriate setup ability in the \'Blue Manual\' operation to hash all the PowerShell ' \
            'Profiles on the Windows machine.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if powershell_profiles_hashed(op):
            return True
    return False


def powershell_profiles_hashed(op):
    return '90a67a85-e81c-4525-8bae-12a2c5787d9a' in [link.ability.ability_id for link in op.chain if link.finish]
