from plugins.training.app.c_flag import Flag


class AdvancedFlag0(Flag):
    name = 'Update configs'
    challenge = 'Update the app.contact.http configuration property to an externally-facing IPv4 address (not 0.0.0.0).'
    extra_info = (
        'C2 servers need to be made accessible to agents, either through agent-network-facing interfaces or proxies. '
        'Changing the app.contact.http configuration value sets the URL that agents will connect to with the HTTP  '
        'contact.'
    )

    async def verify(self, services):
        http_contact = services.get('app_svc').get_config('app.http.contact')
        return not (http_contact.startswith('http://127.0.0.1') or http_contact.startswith('http://0.0.0.0'))
