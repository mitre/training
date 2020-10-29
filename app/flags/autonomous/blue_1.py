from app.utility.base_world import BaseWorld


name = 'Process on Unauthorized Port'
challenge = 'Start a listening process on Port 7011 on the Linux or Darwin machine (`nc -l 7011` should work). The ' \
            'autonomous defender created in the last flag (Incident Responder defender profile, batch planner, and ' \
            'response source) will automatically kill this listener.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Autonomous')):
        if is_unauth_process_detected(op) and is_unauth_process_killed(op):
            return True
    return False


def is_unauth_process_detected(op):
    if all(trait in [f.trait for f in op.all_facts()] for trait in
           ['remote.port.unauthorized', 'host.pid.unauthorized']):
        return True
    return False


def is_unauth_process_killed(op):
    return '02fb7fa9-8886-4330-9e65-fa7bb1bc5271' in [link.ability.ability_id for link in op.chain if link.finish]
