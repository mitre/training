name = 'Bypass authentication'
challenge = 'Ensure that logging in to CALDERA is not required if the browser address is 127.0.0.1'


async def verify(services):
    return '127.0.0.1' in services.get('auth_svc').bypass
