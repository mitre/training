from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find Changes to PowerShell Profile'
challenge = 'Within a minute of this flag activating, a PowerShell Profile will have been modified on the Windows ' \
            'machine. Run the appropriate detection ability in the \'Blue Manual\' operation to find the modified ' \
            'profile.'
extra_info = """"""


operation_name = 'training_manual_5b'
adversary_id = '08619190-9eb5-4f35-97e1-0dafe04e0203'
agent_group = 'cert-win'


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
        if is_modified_profile_found(op):
            return True
    return False


def is_modified_profile_found(op):
    return 'has_been_modified' in [f.trait for f in op.all_facts()] and \
            '930236c2-5397-4868-8c7b-72e294a5a376' in [link.ability.ability_id for link in op.chain if link.finish]
