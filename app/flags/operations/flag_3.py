name = 'Empty operation'
challenge = 'Run a new operation, this time not selecting any profiles or groups. Add at least 5 potential links ' \
              'to the operation.'
extra_info = """When you run an autonomous adversary emulation exercise, the operation can only run the tasks it is pre-configured
to run. Using potential links, you can "toss in" any additional TTPs into a live, autonomous operation. Make sure to end the operation
for the flag status to update."""


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and op.adversary.adversary_id == 'ad-hoc' and len(op.chain) >= 5 and not op.group:
            return True
    return False
