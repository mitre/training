name = 'Add new agent filename'
challenge = 'Ensure that new agents could potentially get named "super_scary.exe" when downloaded on any host. ' \
              'Deploy new agents until one downloads with this name.'


async def verify(services):
    return False
