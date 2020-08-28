from app.utility.base_world import BaseWorld

name = 'Agent filename'
challenge = 'Ensure that new agents will be named "super_scary.exe" when downloaded on any host. ' \
            'Note that the extension is automatically appended.'
extra_info = """Adversaries try to blend in when they compromise a host. One common tactic is to name
their agent after a program that is already running on the host. When defenders check process lists
and file names, the name has a higher chance of blending in."""


async def verify(services):
    if BaseWorld.get_config(name='agents', prop='implant_name') == 'super_scary':
        return True
    return False
