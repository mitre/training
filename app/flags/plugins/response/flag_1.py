from app.utility.base_world import BaseWorld


name = 'Blue operation'
challenge = 'Run a blue operation using the blue agent group, the \'Incident responder\' ' \
            'defender, the batch planner and the response fact source. Before running the operation, start up a listener ' \
            'on port 7011 (using netcat or other, such as "nc -l 7011") on the endpoint with the blue agent.'
extra_info = """EDR agents are intended to run at all times while the endpoint is running. To simulate this, ' \
    'agents can be registered on endpoints to automatically run when the endpoint is booted. Defenders ' \
    'can also be instructed to run continuously through the use of Repeatable abilities."""


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(access=BaseWorld.Access.BLUE)):
        if len(op.agents) and op.group == 'blue' and op.adversary.adversary_id == '7e422753-ad7a-4401-bc8b-b12a28e69c25':
            return is_unauth_process_killed(op)
    return False


def is_unauth_process_detected(operation):
    facts = operation.all_facts()
    return True if any(fact.trait == 'host.pid.unauthorized' for fact in facts) else False


def is_unauth_process_killed(operation):
    return True if any(link.ability.ability_id == '02fb7fa9-8886-4330-9e65-fa7bb1bc5271' for link in operation.chain) \
        else False
