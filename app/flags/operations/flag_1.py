name = 'Base64 operation'
challenge = 'Run a new operation, using any adversary profile - except Hunter - and change the jitter to 10/20 ' \
              'and the obfuscation to base64. At least 5 abilities should execute.'
extra_info = """Just as it is important to use random beacon intervals, adding a random sleep time (jitter) between each command an
agent runs is equally important for staying undetected. Another way to stay undetected is to obfuscate your commands.
Defenders will often write monitors to detect specific keywords used on a host. If an adversary obfuscates their
commands, they can bypass this sort of detection tactic."""


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish and op.adversary.adversary_id != 'de07f52d-9928-4071-9142-cb1d3bd851e8' \
                and op.obfuscator == 'base64' and op.jitter == '10/20' and len(op.chain) >= 5:
            return True
    return False
