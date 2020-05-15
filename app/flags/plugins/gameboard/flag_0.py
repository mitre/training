from datetime import datetime

from app.utility.base_world import BaseWorld

name = 'GameBoard plugin'
challenge = 'Run a red-blue exercise. Create a Red operation named exactly \'Gameboard - Red\', and then run a Blue ' \
            'operation against it named exactly \'Gameboard - Blue\'. The results of this exercise can be seen in ' \
            'the Gameboard plugin modal.'
extra_info = """Purple-teaming is the process of running a red-team engagement in conjunction with the blue-team. It
 is often fruitful to provide some - but not all - of the details between the red and blue teams. This allows both sides
 to train against each other."""


async def verify(services):
    for r in await services.get('data_svc').locate('operations',
                                                   dict(access=BaseWorld.Access.RED, name='Gameboard - Red')):
        for b in await services.get('data_svc').locate('operations',
                                                       dict(access=BaseWorld.Access.BLUE, name='Gameboard - Blue')):
            if r.start < datetime.strptime(b.finish, '%Y-%m-%d %H:%M:%S'):
                return True
    return False
