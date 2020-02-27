name = 'Add new user'
challenge = 'Add new blue-team user credentials for username=test and password=test. Then log in under this user.'


async def verify(services):
    return await services.get('auth_svc').user_map.get('test') is not None
