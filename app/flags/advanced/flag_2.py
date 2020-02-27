name = 'Add new user'
challenge = 'Add new blue-team user credentials for username=test and password=test. Then log in under this user.'


async def verify(services):
    user = services.get('auth_svc').user_map.get('test')
    return 'blue' in user[2]
