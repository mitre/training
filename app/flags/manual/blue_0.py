from app.utility.base_world import BaseWorld


name = 'Enable Manual Operation'
challenge = 'Start a manual blue operation by not specifying any defender profiles. Name this operation exactly ' \
            '\'Blue Manual\'. Keep this operation open to successfully complete the flags for this badge.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if op.adversary.adversary_id == 0:
            return True
    return False
