name = 'Start a UDP agent'
challenge = 'Start a new Manx agent in UDP mode'


async def verify(services):
    for _ in services.get('data_svc').locate('agents', dict(contact='udp')):
        return True
    return False
