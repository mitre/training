name = 'Manx plugin'
challenge = 'Start a new Manx agent on your localhost. Then send at least 2 commands to it through the reverse-shell ' \
              'session. Then run a normal operation against the agent using the Hunter profile.'


async def verify(services):
    check1, check2 = False, False
    for agent in await services.get('data_svc').locate('agents', dict(contact='tcp')):
        history = [entry for entry in services.get('contact_svc').report['websocket'] if entry['paw'] == agent.paw]
        if len(history) > 1:
            check1 = True
        for op in await services.get('data_svc').locate('operations'):
            if op.adversary.adversary_id != 'de07f52d-9928-4071-9142-cb1d3bd851e8':
                continue
            for op_agent in op.agents:
                if op_agent.paw == agent.paw and op.finish:
                    check2 = True
                    break
    return all([check1, check2])
