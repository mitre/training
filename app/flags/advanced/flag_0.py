name = 'Update configurations'
challenge = 'Update the app.contact.http configuration property to http://127.0.0.1:8888 and start a new local agent.'


async def verify(services):
    for agent in await services.get('data_svc').locate('agents'):
        if agent.server == 'http://127.0.0.1':
            return True
    return False

