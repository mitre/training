name = 'Bootstrap abilities'
challenge = 'Using a Stockpile ability, ensure new agents automatically run "whoami" on their first beacon'


async def verify(services):
    return 'c0da588f-79f0-4263-8998-7496b1a40596' in services.get('contact_svc').bootstrap_instructions
