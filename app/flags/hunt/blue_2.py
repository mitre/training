from plugins.training.app.base_flag import BaseFlag


name = 'Hunt Flag 2'
challenge = 'Complete this flag by hunting for the CALDERA ability that will have been run within one minute of this' \
            'flag activating. Once you find the Process ID of the process that ran the PowerShell command(s), enter' \
            'the PID in the Hunt badge, matching the tactic and technique of the procedure that was run. The tactic' \
            'is listed below. The specific technique is listed on the other side of this card as a hint.\n\n' \
            'Tactic: Persistence'
extra_info = """Technique: Boot or Logon Autostart Execution"""


operation_name = 'training_hunt_2'
adversary_id = '5212d9f4-1ad4-4c77-9f8a-55ed8e02d804'
agent_group = 'cert-win'
verify_type = 'pid'


async def verify(services):
    return await BaseFlag.standard_hunt_flag(services, operation_name, adversary_id, agent_group, verify_type)
