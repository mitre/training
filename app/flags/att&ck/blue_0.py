name = 'ATT&CK Quiz 1'
challenge = 'This badge tests your knowledge of ATT&CK techniques. Complete the challenge by determining the one ' \
            'ATT&CK technique that best matches the procedure on the back of this card. Select this technique in ' \
            'the Compass plugin, and download the layer. Rename the downloaded JSON file as exactly ' \
            '\'blue_quiz_1.json\', and upload it to the server by selecting \'Upload Adversary Layer\''
extra_info = """whoami"""


async def verify(services):
    adversaries = await services.get('data_svc').locate('adversaries', match=dict(name='blue_quiz_1'))
    technique = 'System Owner/User Discovery'
    for adv in adversaries:
        match = await does_technique_match(services.get('data_svc', adv, technique))
        services.get('rest_svc').delete_adversary(adv.adversary_id)
        if match:

            return True
    return False


async def does_technique_match(data_svc, adv, technique):
    techniques = set()
    for ab_id in adv.atomic_ordering:
        for abilities in await data_svc.locate('abilities', match=dict(ability_id=ab_id)):
            techniques.update([ab.technique_id for ab in abilities])
    return technique in techniques
