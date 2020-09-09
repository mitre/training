from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find suspicious URL in mail'
challenge = 'Within a minute of this flag activating, a pretend phishing email with a malicious URL will have been ' \
            'sent on the *nix machine. Run the appropriate detection ability in the \'Blue Manual\' operation to ' \
            'find this URL.'
extra_info = """"""


_operation_name = 'training_manual_3'
_adversary_id = '2c99958e-36e0-4fab-bcdf-977926a58cd6'
_agent_group = 'cert-nix'


async def verify(services):
    return await BaseFlag.standard_verify_with_operation(services, _operation_name, _adversary_id, _agent_group,
                                                         _is_flag_satisfied)


async def _is_flag_satisfied(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if _is_url_found(op):
            return True
    return False


def _is_url_found(op):
    return 'remote.suspicious.url' in [f.trait for f in op.all_facts()] and \
            '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce' in [link.ability.ability_id for link in op.chain if link.finish]
