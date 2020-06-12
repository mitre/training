from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find New Unauthorized Scheduled Task'
challenge = 'Within a minute of this flag activating, a new scheduled task will have been registered on the windows ' \
            'machine. Run the appropriate detection ability in the \'Blue Manual\' operation to find this cron job.'
extra_info = """"""


operation_name = 'training_manual_4b'
adversary_id = '9fbc7164-9175-4fc6-bb20-9669dc121df8'
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
        if is_cronjob_found(op):
            return True
    return False


def is_cronjob_found(op):
    return 'host.new.schtask' in [f.trait for f in op.all_facts()] and \
            '8bc73098-54d1-4f69-abd5-271e3e2da5df' in [link.ability.ability_id for link in op.chain if link.finish]
