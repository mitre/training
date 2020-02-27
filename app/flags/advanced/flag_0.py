name = 'Update configurations'
challenge = 'Update the app.contact.http configuration property to the local ipv4 address and start a new local agent ' \
            'using this address'


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if agent.server != 'http://127.0.0.1:8888':
            return True
    return False

