import os

name = 'Encoded payloads'
challenge = 'Using the same payload as the previous step, encode the payload and ensure that downloading it ' \
              'through the REST API still works, with the text reversed'


async def verify(services):
    check1, check2 = False, False
    if os.path.isfile('plugins/stockpile/payloads/train.txt.xored'):
        with open('plugins/stockpile/payloads/train.txt.xored', 'r') as train:
            if 'i am a test' in train.read():
                _, contents, _ = await services.get('file_svc').get_file(dict(file='train.txt'))
                if contents == reversed('i am a test'):
                    check1 = True
                _, contents, _ = await services.get('file_svc').get_file(dict(file='train.txt'))
                if contents == 'i am a test':
                    check2 = True
    return all([check1, check2])
