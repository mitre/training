from plugins.training.app.base_flag import BaseFlag

name = 'ATT&CK Quiz 4'
challenge = 'Refer to \'ATT&CK Quiz 1\' for instructions. Name the uploaded adversary layer exactly \'blue_quiz_4\'. ' \
            'Ensure that you\'re starting from a fresh layer on the Compass plugin.\n\n' \
            'The adversary procedure is:\nImport-Module .\\invoke-mimi.ps1; Invoke-Mimikatz -DumpCreds'
extra_info = ''

technique = 'T1003'  # Credential Dumping
adv_name = 'blue_quiz_4'


async def verify(services):
    return await BaseFlag.verify_attack_flag(services, technique, adv_name)
