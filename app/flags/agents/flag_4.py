from app.utility.base_world import BaseWorld

name = 'Add new agent filename'
challenge = 'Ensure that new agents will be named "super_scary.txt" when downloaded on any host.'


async def verify(services):
    if BaseWorld.get_config(name='agents', prop='implant_name') == 'super_scary.txt':
        return True
    return False
