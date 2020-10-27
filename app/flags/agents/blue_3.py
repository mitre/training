name = 'Blue agent - Windows'
challenge = 'Deploy a blue agent on a Windows machine. Ensure that this agent has ELEVATED privileges. ' \
            'This agent will be used in later challenges.'
extra_info = """"""


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if 'win' in agent.platform and agent.group == 'blue' and agent.privilege == 'Elevated':
            return True
    return False
