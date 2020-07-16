from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Flag 3'
challenge = ''
extra_info = """"""


operation_name = 'training_hunt_3'
adversary_id = 'c25160e6-7d8d-490c-94cf-95944e46f885'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
