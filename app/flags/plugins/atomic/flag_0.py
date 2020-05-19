name = 'Atomic plugin'
challenge = 'As a red user, enable the Atomic plugin and verify that new abilities have been added to the database'
extra_info = """There are lots of sources for TTPs on the Internet, and more are added daily. These TTPs can be in any format and in
any language. It is possible, and often trivial, to import them into CALDERA for use in operations."""


async def verify(services):
    for _ in await services.get('data_svc').locate('plugins', dict(enabled=True, name='atomic')):
        return True
    return False
