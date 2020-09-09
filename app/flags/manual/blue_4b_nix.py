from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find New Unauthorized Cron Job'
challenge = 'Within a minute of this flag activating, a new cron job will have been installed on the *nix machine. ' \
            'Run the appropriate detection ability in the \'Blue Manual\' operation to find this cron job.'
extra_info = """"""


_operation_name = 'training_manual_4a'
_adversary_id = '9fbc7164-9175-4fc6-bb20-9669dc121df8'
_agent_group = 'cert-nix'


async def verify(services):
    return await BaseFlag.standard_verify_with_operation(services, _operation_name, _adversary_id, _agent_group,
                                                         _is_flag_satisfied)


async def _is_flag_satisfied(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if _is_cronjob_found(op):
            return True
    return False


def _is_cronjob_found(op):
    return all(trait in [f.trait for f in op.all_facts()] for trait in ['host.user.name', 'host.new.cronjob']) and \
            'ee54384f-cfbc-4228-9dc1-cc5632307afb' in [link.ability.ability_id for link in op.chain if link.finish]
