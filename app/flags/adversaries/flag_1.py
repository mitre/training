name = 'Add a pack'
challenge = 'Add the Nosy Neighbor adversary pack to the Super Spy adversary and save it'


async def verify(services):
    for a in await services.get('data_svc').locate('adversaries', dict(adversary_id='564ae20d-778d-4965-93dc-b523be2e2ab4')):
        for _, abilities in a.phases.items():
            for ability in abilities:
                if ability.ability_id == '2fe2d5e6-7b06-4fc0-bf71-6966a1226731':
                    return True
    return False
