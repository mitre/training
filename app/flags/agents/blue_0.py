name = 'Red agent - *nix'
challenge = 'Deploy a red agent on a Linux or Mac machine. This agent will be used in later challenges.'
extra_info = """"""


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if agent.platform in ['linux', 'darwin'] and agent.group != 'blue':
            return True
    return False
