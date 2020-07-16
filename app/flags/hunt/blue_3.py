from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Flag 3'
challenge = 'Complete this flag by hunting for the CALDERA ability that will have been run within one minute of this' \
            'flag activating. Once you find the Process ID of the process that ran the PowerShell command(s), enter' \
            'the PID in the Hunt badge, matching the tactic and technique of the procedure that was run. The tactic' \
            'is listed below. The specific technique is listed on the other side of this card as a hint.\n\n' \
            'Tactic: Defense Evasion'
extra_info = """Technique: Modify Registry"""


operation_name = 'training_hunt_3'
adversary_id = 'c25160e6-7d8d-490c-94cf-95944e46f885'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
