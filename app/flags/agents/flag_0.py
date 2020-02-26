name = 'Local 54ndc47 agent'
description = 'Demonstrate your ability to deploy a 54ndc47 agent on local host. The agent should successfully ' \
              'beacon back to this server instance.'


async def verify(services):
    return len(await services.get('data_svc').locate('agents')) > 0
