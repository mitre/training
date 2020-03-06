name = 'Manual operation'
challenge = 'Run a new operation, using any adversary profile - except Hunter - and run the operation requiring ' \
              'manual approval. Approve and discard links as desired.'
extra_info = """
Sometimes, in an adversary emulation exercise, you may want to approve every command before it is tasked to an agent. 
This allows you to ensure it doesn't do anything you don't want it to.
"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and op.adversary.adversary_id != 'de07f52d-9928-4071-9142-cb1d3bd851e8' and not op.autonomous:
            return True
    return False
