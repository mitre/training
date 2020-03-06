from app.utility.base_world import BaseWorld

name = 'Bootstrap abilities'
challenge = 'Using a Stockpile ability, ensure new agents automatically run "whoami" on their first beacon'


async def verify(services):
    abilities = BaseWorld.get_config(name='agents', prop='bootstrap_abilities')
    return 'c0da588f-79f0-4263-8998-7496b1a40596' in abilities
