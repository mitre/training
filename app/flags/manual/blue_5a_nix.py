from app.utility.base_world import BaseWorld


name = 'Backup Bash Profiles'
challenge = 'Run the appropriate setup ability in the \'Blue Manual\' operation to backup all the Bash Profiles on ' \
            'the *nix machine.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if bash_profiles_backed_up(op):
            return True
    return False


def bash_profiles_backed_up(op):
    return '622e4bda-e5a8-42bb-93d9-a7b1eebc7e41' in [link.ability.ability_id for link in op.chain if link.finish]
