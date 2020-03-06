from app.utility.base_world import BaseWorld

name = 'Add new agent filename'
challenge = 'Ensure that new agents will be named "super_scary.txt" when downloaded on any host.'
extra_info = """Adversaries try to blend in when they compromise a host. One common tactic is to name their agent after a program 
that is already running on the host. When defenders check process lists and file names, the name has a higher 
chance of blending in."""


async def verify(services):
    if BaseWorld.get_config(name='agents', prop='implant_name') == 'super_scary.txt':
        return True
    return False
