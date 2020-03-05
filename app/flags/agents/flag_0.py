name = 'Deploy local agent'
challenge = 'Demonstrate your ability to deploy an agent on local host. The agent should successfully ' \
              'beacon back to this server instance.'


async def verify(services):
    return len(await services.get('data_svc').locate('agents')) > 0
