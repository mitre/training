name = 'Compass plugin'
challenge = 'In the Compass plugin, create a new adversary'
extra_info = """Before an adversary emulation exercise, it may be helpful to display the adversary you plan on running on the 
ATT&CK matrix. The matrix will highlight each TTP contained in the adversary profile."""


async def verify(services):
    for a in await services.get('data_svc').locate('adversaries'):
        if 'compass' in a.description:
            return True
    return False
