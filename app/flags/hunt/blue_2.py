from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Flag 2'
challenge = ''
extra_info = """"""


operation_name = 'training_hunt_2'
adversary_id = '5212d9f4-1ad4-4c77-9f8a-55ed8e02d804'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
