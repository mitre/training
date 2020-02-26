import sys

name = 'Remote 54ndc47 agent'
description = 'Demonstrate your ability to deploy a 54ndc47 agent on a remote host. The agent should successfully ' \
              'beacon back to this server instance. This agent should be run on an operating system that is NOT the ' \
              'same as what is hosting the server. It is OK to use a virtual box to complete this challenge.'


async def verify(services):
    agents = await services.get('data_svc').locate('agents')
    check1 = len(agents) > 1
    check2, check3 = False, False
    for a in agents:
        if a.platform != sys.platform:
            check2 = True
        if a.server not in ['127.0.0.1', 'localhost', '0.0.0.0']:
            check3 = True
    return all([check1, check2, check3])
