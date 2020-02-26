name = 'Special payloads'
challenge = 'Add a new payload (anywhere) as a text file with the contents "i am a test" and mark it as a ' \
              'special payload. When downloaded through the REST api, the payload should return the file with ' \
              'the text inside reversed.'


async def verify(services):
    return False
