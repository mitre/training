name = 'Update configurations'
challenge = 'Update the app.contact.http configuration property to the local ipv4 address'


async def verify(services):
    http_contact = services.get('app_svc').get_config('app.http.contact')
    if http_contact != 'http://127.0.0.1:8888':
        return True
    return False

