from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Detect process on Unauthorized Port'
challenge = 'Start a listening process on Port 7011 on the Linux or Darwin machine. Run the appropriate detection ' \
            'ability in the \'Blue Manual\' operation to detect this process.'
extra_info = """"""

operation_name = 'training_manual_1'
adversary_id = '6e19d5f9-e4d9-42b2-bc89-ea4298541d80'
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
        if is_unauth_process_detected(op):
            return True
    return False


def is_unauth_process_detected(op):
    if all(trait in [f.trait for f in op.all_facts()] for trait in
           ['remote.port.unauthorized', 'host.pid.unauthorized']):
        return True
    return False
