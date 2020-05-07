from app.utility.base_world import BaseWorld


name = 'Detect malicious file on system'
challenge = 'Write a file on the Windows machine under the C:\\Users directory. Get the SHA256 hash of this file, ' \
            'and write it to C:\\Users\\Public\\malicious_files.txt. Run the appropriate detection ability in the ' \
            '\'Blue Manual\' operation to detect this file hash.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if is_file_detected(op):
            return True
    return False


def is_file_detected(op):
    return 'file.malicious.hash' in [f.trait for f in op.all_facts()] and \
            '77272c88-ccf5-4225-a3d9-f9e171d1ca5b' in [link.ability.ability_id for link in op.chain if link.finish]
