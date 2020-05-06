from app.utility.base_world import BaseWorld


name = 'Detect process on Unauthorized Port'
challenge = 'Start a listening process on Port 7011 on the Linux or Darwin machine. Run the appropriate detection ' \
            'ability in the \'Blue Manual\' operation to detect this process.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_unauth_process_detected(op):
            return True
    return False


def is_unauth_process_detected(op):
    if all(trait in [f.trait for f in op.all_facts] for trait in ['host.unauthorized.port', 'host.pid.unauthorized']):
        return True
    return False
