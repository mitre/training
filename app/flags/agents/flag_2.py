name = 'Understanding untrusted'
challenge = 'Change the untrusted agent timer to 90 seconds. Then ensure one of your agents becomes untrusted.'


async def verify(services):
    if services.get('contact_svc').untrusted_timer == 90:
        return True
    return False
