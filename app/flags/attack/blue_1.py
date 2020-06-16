from plugins.training.app.base_flag import BaseFlag

name = 'ATT&CK Quiz 2'
challenge = 'Refer to \'ATT&CK Quiz 1\' for instructions. Name the uploaded adversary layer exactly \'blue_quiz_2\'. ' \
            'Ensure that you\'re starting from a fresh layer on the Compass plugin.\n\n' \
            'The adversary procedure is:\nGet-ChildItem -Path #{host.system.path}'
extra_info = ''

technique = 'T1083'  # File and Directory Discovery
adv_name = 'blue_quiz_2'


async def verify(services):
    return await BaseFlag.verify_attack_flag(services, technique, adv_name)
