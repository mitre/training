from plugins.training.app.base_flag import BaseFlag


name = "Initialize Hunt Badge"
challenge = 'This flag tests the environment to ensure the rest of the Hunt badge works correctly. This flag will ' \
            'pass only if the following conditions are met:\n\n' \
            '1) The Hunt plugin is enable in Caldera.\n' \
            '2) The target Windows machine has Sysmon running.'
extra_info = """"""

operation_name = 'hunt_initialize'
adversary_id = 'b2d8e29a-fb11-4ba7-bde4-60d9a628784e'
agent_group = 'cert-win'


async def verify(services):
    return await BaseFlag.standard_verify_with_operation(services, operation_name, adversary_id, agent_group,
                                                         is_flag_satisfied)


async def is_flag_satisfied(services):
    return hunt_available(services) and await sysmon_available(services)


def hunt_available(services):
    return 'hunt_svc' in services


async def sysmon_available(services):
    ops = await services.get('data_svc').locate('operations', match=dict(name=operation_name))
    for op in ops:
        if 'host.process.name' in [fact.trait for fact in op.all_facts()]:
            return True
    return False
