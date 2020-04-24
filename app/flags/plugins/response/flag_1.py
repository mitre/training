name = 'Blue operation'
challenge = 'Run a blue operation using the previously deployed blue agent and the \'Incident responder\' ' \
            'adversary/defender.'
extra_info = """EDR agents are intended to run at all times while the endpoint is running. To simulate this, Caldera 
agents can be registered on endpoints to automatically run when the endpoint is started. Caldera Defenders/Adversaries 
can also be instructed to run continuously through the use of repeatable abilities."""

async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and len(op.agents) and op.group == 'blue' \
                and op.adversary.adversary_id == '7e422753-ad7a-4401-bc8b-b12a28e69c25':
            return True
    return False