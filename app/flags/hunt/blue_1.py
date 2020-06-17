from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Test'
challenge = ''
extra_info = """"""


operation_name = 'Hunt1'
adversary_id = '1a8218e4-c7b7-424a-befb-48b3421d2e78'
agent_group = 'cert-nix'


async def verify(services):
    return await BaseFlag.standard_verify_with_operation(services, operation_name, adversary_id, agent_group,
                                                         is_flag_satisfied)


async def is_flag_satisfied(services):
    link_pid = (await services.get('data_svc').locate('operations', match=dict(name=operation_name)))[0].chain[0].pid
    if services.get('hunt_svc').is_pid_verified(link_pid):
        return True
    return False
