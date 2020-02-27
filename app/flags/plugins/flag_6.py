from app.utility.base_world import BaseWorld

name = 'Understanding access'
challenge = 'Change the access of the GameBoard plugin so only blue-team users can access it'


async def verify(services):
    for plugin in await services.get('data_svc').locate('plugins', dict(name='GameBoard')):
        return plugin.access == BaseWorld.Access.BLUE
    return False
