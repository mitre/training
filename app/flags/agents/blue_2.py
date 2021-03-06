name = 'Red agent - Windows'
challenge = 'Deploy a red agent on a Windows machine with a group named exactly \'cert-win\'. This agent will be used' \
            ' in later challenges.'
extra_info = """"""


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if 'win' in agent.platform and agent.group == 'cert-win':
            return True
    return False
