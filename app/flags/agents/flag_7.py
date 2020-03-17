name = 'Agent watchdog'
challenge = 'Using watchdog, kill one of your agents'
extra_info = """In red-team engagements, operators often need to clean up the environments under test at the end
of the testing. Going through box-by-box can be time-consuming, so using automation to auto-stop agents is preferred. """


async def verify(services):
    for a in await services.get('data_svc').locate('agents'):
        if a.watchdog > 0:
            return True
    return False
