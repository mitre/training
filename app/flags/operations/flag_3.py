name = 'Empty operation'
challenge = 'Run a new operation, this time not selecting any profiles or groups. Add at least 5 potential links ' \
              'to the operation.'


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and op.adversary.adversary_id == 0 and len(op.chain) >= 5 and not op.group:
            return True
    return False
