name = 'Write new parser'
challenge = 'Add a new parser which parses IPV6 addresses with the trait, "host.ip.ipv6". ' \
              'Then run an adversary which correctly parses out matching facts. Hint: use the ability you created ' \
            'in an earlier flag.'


async def verify(services):
    for op in await services.get('data_svc').locate('operations'):
        if op.finish:
            found_fact = [fact for fact in op.all_facts() if fact.trait == 'host.ip.ipv6'
                          and len(fact.value.split(':')) == 8]
            if len(found_fact) > 0:
                return True
    return False
