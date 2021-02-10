from plugins.training.app.c_flag import Flag


class AdvancedFlag2(Flag):
    name = 'Add new user'
    challenge = 'Add new red-team user credentials, using "test" as both the username and password. Make sure ' \
                'the server is turned off before editing the configuration files.'
    extra_info = """In a red-team engagement, there are usually multiple operators sharing access to the C2."""

    async def verify(self, services):
        user = services.get('auth_svc').user_map.get('test')
        return user and user.password == 'test' and 'red' in user.permissions
