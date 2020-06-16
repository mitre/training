from plugins.training.app.base_flag import BaseFlag

name = 'ATT&CK Quiz 5'
challenge = 'Refer to \'ATT&CK Quiz 1\' for instructions. Name the uploaded adversary layer exactly \'blue_quiz_5\'. ' \
            'Ensure that you\'re starting from a fresh layer on the Compass plugin.\n\n' \
            'The adversary procedure is:\nnet /y use \\#{remote.host.name} &' \
            '\ncopy /y sandcat.go-windows\n\\\\#{remote.host.name}\\Users\\Public'
extra_info = ''

technique = 'T1105'  # Remote File Copy
adv_name = 'blue_quiz_5'


async def verify(services):
    return await BaseFlag.verify_attack_flag(services, technique, adv_name)
