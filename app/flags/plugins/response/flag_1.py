from app.utility.base_world import BaseWorld


name = 'Blue operation'
challenge = 'Using the machine with the blue agent, connect to a listener on another machine listening on TCP ' \
            'port 7011. This can be done using Netcat on *nix machines, or TcpClient on Windows machines.' \
            'Then, run a blue operation using the blue agent group, the \'Incident responder\' defender, the batch ' \
            'planner and the response fact source.'
extra_info = 'EDR agents are intended to run at all times while the endpoint is running. To simulate this, ' \
             'agents can be registered on endpoints to automatically run when the endpoint is booted. Defenders ' \
             'can also be instructed to run continuously through the use of Repeatable abilities.'


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(access=BaseWorld.Access.BLUE)):
        if len(op.agents) and op.group == 'blue' and \
                op.adversary.adversary_id == '7e422753-ad7a-4401-bc8b-b12a28e69c25':
            if is_unauth_process_killed(op):
                return True
    return False


def is_unauth_process_detected(operation):
    facts = operation.all_facts()
    return True if any(fact.trait == 'host.pid.unauthorized' for fact in facts) else False


def is_unauth_process_killed(operation):
    return True if any(link.ability.ability_id == '02fb7fa9-8886-4330-9e65-fa7bb1bc5271' for link in operation.chain) \
        else False
