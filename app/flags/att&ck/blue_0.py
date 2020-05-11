name = 'ATT&CK Quiz 1'
challenge = 'This badge tests your knowledge of ATT&CK techniques. Look on the back of this card for instructions ' \
            'on how to complete the challenge. Each of the following challenges in this badge will follow the same' \
            ' process. Ensure the uploaded adversary is named exactly \'blue_quiz_1\'.\n\n' \
            'The adversary procedure is:\nwhoami'
extra_info = """Complete the challenge by determining the one ATT&CK technique that best matches the procedure on the
 front of this card. Select this technique in the Compass plugin on the red side of CALDERA, and download the layer.
 Rename the downloaded JSON file as indicated on the front of this card, and upload it to the server by selecting
 \'Upload Adversary Layer\'. Use the help button on the Compass plugin modal for reference."""


async def verify(services):
    adversaries = await services.get('data_svc').locate('adversaries', match=dict(name='blue_quiz_1'))
    technique = 'T1033'  # System Owner User Discovery
    for adv in adversaries:
        match = await does_technique_match(services, adv, technique)
        await services.get('rest_svc').delete_adversary(dict(adversary_id=adv.adversary_id))
        if match:
            return True
    return False


async def does_technique_match(services, adv, technique):
    techniques = set()
    for ab_id in adv.atomic_ordering:
        techniques.add((await services.get('rest_svc').display_objects('abilities',
                                                                       data=dict(ability_id=ab_id)))[0]['technique_id'])
    return technique in techniques and len(techniques) == 1
