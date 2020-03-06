name = 'Add new user'
challenge = 'Add new red-team user credentials for username=test and password=test. Then log in under this user.'
extra_info = """In a red-team engagement, there are usually multiple operators sharing access to the C2."""


async def verify(services):
    user = services.get('auth_svc').user_map.get('test')
    return 'red' in user[2]
