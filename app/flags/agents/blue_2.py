name = 'Red agent - Windows'
challenge = 'Deploy a red agent on a Windows machine. This agent will be used in later challenges.'
extra_info = """"""


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if 'win' in agent.platform and agent.group != 'blue':
            return True
    return False
