name = 'Update agent'
challenge = 'Pick any agent and change the group and sleep (min and max) values associated to it'


async def verify(services):
    for a in await services.get('data_svc').locate('agents'):
        if a.group != 'red' and a.sleep_min != 30 and a.sleep_max != 60:
            return True
    return False
