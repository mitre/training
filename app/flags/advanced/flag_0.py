name = 'Update configs'
challenge = 'Update the app.contact.http configuration property to the local ipv4 address'
extra_info = """Adversaries will often make their C2 server available behind a proxy. Doing this allows them to hide their own IP
address while maintaining local control of the server on their local machine."""


async def verify(services):
    http_contact = services.get('app_svc').get_config('app.http.contact')
    if http_contact != 'http://127.0.0.1:8888':
        return True
    return False
