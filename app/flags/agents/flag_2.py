from app.utility.base_world import BaseWorld

name = 'Understanding untrusted'
challenge = 'Change the untrusted agent timer to 90 seconds.'


async def verify(services):
    if BaseWorld.get_config(name='agents', prop='untrusted_timer') == 90:
        return True
    return False
