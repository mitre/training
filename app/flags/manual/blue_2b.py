from app.utility.base_world import BaseWorld
from plugins.training.app.c_flag import Flag


class ManualBlue2b(Flag):
    name = 'Hunt for malicious file on system'
    challenge = 'Run the appropriate hunt ability in the \'Blue Manual\' operation to find the location of the ' \
                'malicious file.'
    extra_info = """"""

    async def verify(self, services):
        for op in await services.get('data_svc').locate('operations',
                                                        match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
            if self._is_file_found(op):
                return True
        return False
