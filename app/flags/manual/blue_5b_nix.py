from app.utility.base_world import BaseWorld


name = 'Acquire Bash Profile Hashes'
challenge = 'Run the appropriate setup ability in the \'Blue Manual\' operation to hash all the Bash Profiles on ' \
            'the *nix machine.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if bash_profiles_hashed(op):
            return True
    return False


def bash_profiles_hashed(op):
    return 'df9d2b83-b40f-4167-af75-31ddde59af7e' in [link.ability.ability_id for link in op.chain if link.finish]
