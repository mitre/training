import requests

name = 'Create a new plugin'
challenge = 'Build a new plugin named "abilities" where a GUI page displays all the ability IDs which are ' \
              'in the database. Ensure this plugin is available at /plugin/abilities/gui'


async def verify(services):
    check1, check2 = False, False
    for _ in await services.get('data_svc').locate('plugins', dict(enabled=True, name='abilities')):
        #abilities = services.get('data_svc').locate('abilities')
        result = requests.get('http://127.0.0.1:8888/plugin/abilities/gui')
        print(result.text())
    return all([check1, check2])
