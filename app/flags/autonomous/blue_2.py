from app.utility.base_world import BaseWorld


name = 'Malicious file on system'
challenge = 'Write a file on the Windows machine under the C:\\Users directory. Get the SHA256 hash of this file, ' \
            'and write it to C:\\Users\\Public\\malicious_files.txt. The autonomous defender should ' \
            'automatically find and delete the file.'
extra_info = """"""


async def verify(services):
    for op in services.get_service('data_svc').locate('operations',
                                                      match=dict(access=BaseWorld.Access.BLUE), name='Blue Autonomous'):
        if is_file_found(op) and is_file_deleted(op):
            return True
    return False


def is_file_found(op):
    if all(trait in [f.trait for f in op.all_facts] for trait in ['file.malicious.hash', 'host.malicious.file']):
        return True
    return False


def is_file_deleted(op):
    return True if '5ec7ae3b-c909-41bb-9b6b-dadec409cd40' in [link.ability.ability_id for link in op.chain] else False
