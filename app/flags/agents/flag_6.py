from app.utility.base_world import BaseWorld

name = 'New contact point'
challenge = 'Deploy a new agent, using a different contact point then your first agent'


async def verify(services):
    contacts = set([agent.contact for agent in await services.get('data_svc').locate('agents')])
    if len(contacts) > 1:
        return True
    return False
