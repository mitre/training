from app.utility.base_world import BaseWorld


name = 'Inoculate suspicious URL'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to inoculate this URL.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE), name='Blue Autonomous'):
        if is_url_inoculated(op):
            return True
    return False


def is_url_inoculated(op):
    return '2ca64acd-dc12-4cc8-b78a-6a182508a50b' in [link.ability.ability_id for link in op.chain if link.finish]
