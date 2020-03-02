name = 'Build an agent'
challenge = 'Create a new Linux/MacOS agent, using the HTTP contact. This agent should use a new executor - zsh. ' \
            'You will need to add at least 1 matching zsh ability. Run a new operation against this agent, running ' \
            'the new ability.'


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if len(op.chain) > 0:
            for agent in op.agents:
                if agent.executors == ['zsh']:
                    return True
    return False
