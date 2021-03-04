from app.utility.base_world import BaseWorld
from plugins.training.app.c_flag import Flag


class PluginsGameboardFlag0(Flag):
    name = 'GameBoard plugin'

    challenge = (
        'Run a red-blue exercise. Create a red operation named "Gameboard - Red", and a blue operation named '
        '"Gameboard - Blue". View the results in the Gameboard plugin.'
    )

    extra_info = (
        'Purple-teaming is the process of running a red-team engagement in conjunction with the blue-team. It is often '
        'fruitful to provide some - but not all - of the details between the red and blue teams. This allows both '
        'sides to train against each other.'
    )

    async def verify(self, services):
        plugin = await services.get('data_svc').locate('plugins', match=dict(enabled=True, name='gameboard'))
        red = await services.get('data_svc').locate('operations', dict(access=BaseWorld.Access.RED,
                                                                       name='Gameboard - Red'))
        blue = await services.get('data_svc').locate('operations', dict(access=BaseWorld.Access.BLUE,
                                                                        name='Gameboard - Blue'))
        return bool(plugin and red and blue)
