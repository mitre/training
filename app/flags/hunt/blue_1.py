from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Flag 1'
challenge = 'Complete this flag by hunting for the CALDERA ability that will have been run within one minute of this ' \
            'flag activating. Submit the PID of the process in the Hunt plugin along with the relevant ATT&CK ' \
            'information. The tactic is listed below. The technique is listed on the back of this ' \
            'card as a hint.\n\n' \
            'Tactic: Command and Control'
extra_info = """Technique: Ingress Tool Transfer"""


operation_name = 'training_hunt_1'
adversary_id = '1a8218e4-c7b7-424a-befb-48b3421d2e78'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
