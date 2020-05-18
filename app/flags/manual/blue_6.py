from plugins.training.app.base_flag import BaseFlag
from app.utility.base_world import BaseWorld


name = 'Find suspicious URL in mail'
challenge = 'Use the \'mail\' utility to send an email to a user on the Linux or Darwin machine. Spoof the sender ' \
            'address to be an email address with a fake malicious domain. Run the appropriate detection ' \
            'ability in the \'Blue Manual\' operation to find this URL.'
extra_info = """"""


operation_name = 'training_manual_3'
adversary_id = '2c99958e-36e0-4fab-bcdf-977926a58cd6'
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
        if is_url_found(op):
            return True
    return False


def is_url_found(op):
    return 'remote.suspicious.url' in [f.trait for f in op.all_facts()] and \
            '1226f8ec-e2e5-4311-88e7-378c0e5cc7ce' in [link.ability.ability_id for link in op.chain if link.finish]
