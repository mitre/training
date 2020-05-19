from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Detect malicious file on system'
challenge = 'Within a minute of this flag activating, a pretend malicious file will have been written on the ' \
            'Windows machine. The hash of this file will also have been written into ' \
            'C:\\Users\\Public\\malicious_files.txt. Run the appropriate detection ability in the \'Blue Manual\' ' \
            'operation to detect this file hash.'
extra_info = """"""


operation_name = 'training_manual_2'
adversary_id = '890508db-9646-4a2d-8d1a-4ea25b3ce02a'
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
        if is_file_detected(op):
            return True
    return False


def is_file_detected(op):
    return 'file.malicious.hash' in [f.trait for f in op.all_facts()] and \
            '77272c88-ccf5-4225-a3d9-f9e171d1ca5b' in [link.ability.ability_id for link in op.chain if link.finish]
