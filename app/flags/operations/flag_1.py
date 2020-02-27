name = 'Run another operation'
challenge = 'Run a new operation, using any adversary profile - except Hunter - and change the jitter to 10/20 ' \
              'and the obfuscation to base64'


async def verify(services):
    for op in await services.get('data_svc').locate('operations', dict(name='operations')):
        if op.finish and op.adversary.adversary_id != 'de07f52d-9928-4071-9142-cb1d3bd851e8' \
                and op.obfuscator == 'base64' and op.jitter == '10/20':
            return True
    return False
