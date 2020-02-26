name = 'Add new agent filename'
challenge = 'Ensure that new agents could potentially get named "super_scary.exe" when downloaded on any host. ' \
              'Deploy new agents until one downloads with this name.'


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if agent.exe_name == 'super_scary.exe':
            return True
    return False
