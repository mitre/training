name = "Initialize Hunt Badge"
challenge = 'This flag tests the environment to ensure the rest of the Hunt badge works correctly. This flag will ' \
            'pass only if the GameBoard plugin is enabled in Caldera.'
extra_info = """"""


async def verify(services):
    return 'gameboard_svc' in services
