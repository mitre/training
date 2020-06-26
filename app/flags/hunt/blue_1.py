from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Test'
challenge = ''
extra_info = """"""


operation_name = 'Hunt1'
adversary_id = '1a8218e4-c7b7-424a-befb-48b3421d2e78'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
