from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Inoculate suspicious URL'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to inoculate the previously ' \
            'found URL.'
extra_info = """"""


operation_name = 'training_manual_3_cleanup'
adversary_id = '2885d0fe-60a7-469b-9e2e-a46b7be2b4df'
agent_group = 'cert-nix'


async def verify(services):
    if await BaseFlag.does_agent_exist(services, agent_group):
        if not (await BaseFlag.is_operation_started(services, operation_name)):
            await BaseFlag.start_operation(services, operation_name, agent_group, adversary_id)
        if await BaseFlag.is_operation_successful(services, operation_name) and await is_flag_satisfied(services):
            await BaseFlag.cleanup_operation(services, operation_name)
            return True
    return False


async def is_flag_satisfied(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_url_inoculated(op):
            return True
    return False


def is_url_inoculated(op):
    return '2ca64acd-dc12-4cc8-b78a-6a182508a50b' in [link.ability.ability_id for link in op.chain if link.finish]
