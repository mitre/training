name = 'Terminal plugin'
description = 'Start a new Manx agent on your localhost. Then send at least 2 commands to it through the reverse-shell ' \
              'session. Then run a normal operation against the agent using the Hunter profile.'


async def verify(services):
    return False
