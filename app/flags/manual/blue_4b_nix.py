from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find New Unauthorized Cron Job'
challenge = 'Within a minute of this flag activating, a new cron job will have been installed on the *nix machine. ' \
            'Run the appropriate detection ability in the \'Blue Manual\' operation to find this cron job.'
extra_info = """"""


operation_name = 'training_manual_4a'
adversary_id = '9fbc7164-9175-4fc6-bb20-9669dc121df8'
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
        if is_cronjob_found(op):
            return True
    return False


def is_cronjob_found(op):
    return all(trait in [f.trait for f in op.all_facts()] for trait in ['host.user.name', 'host.new.cronjob']) and \
            'ee54384f-cfbc-4228-9dc1-cc5632307afb' in [link.ability.ability_id for link in op.chain if link.finish]
