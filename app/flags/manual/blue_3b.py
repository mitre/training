from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Inoculate suspicious URL'
challenge = 'Run the appropriate response ability in the \'Blue Manual\' operation to inoculate the previously ' \
            'found URL.'
extra_info = """"""


_operation_name = 'training_manual_3_cleanup'
_adversary_id = '2885d0fe-60a7-469b-9e2e-a46b7be2b4df'
_agent_group = 'cert-nix'


async def verify(services):
    return await BaseFlag.standard_verify_with_operation(services, _operation_name, _adversary_id, _agent_group,
                                                         _is_flag_satisfied)


async def _is_flag_satisfied(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if _is_url_inoculated(op):
            return True
    return False


def _is_url_inoculated(op):
    return '2ca64acd-dc12-4cc8-b78a-6a182508a50b' in [link.ability.ability_id for link in op.chain if link.finish]
