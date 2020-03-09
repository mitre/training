from app.utility.payload_encoder import xor_file


class Encoder:

    def __init__(self):
        self.encoded_cert_path = 'plugins/training/static/img/caldera.cert.encoded'
        self.decoded_cert_path = 'plugins/training/static/img/caldera.cert.decoded.png'

    async def decode_cert(self, certify_key):
        await self.xor_cert(certify_key=certify_key,
                            input_file=self.encoded_cert_path,
                            output_file=self.decoded_cert_path)

    async def encode_cert(self, certify_key):
        await self.xor_cert(certify_key=certify_key,
                            input_file=self.decoded_cert_path,
                            output_file=self.encoded_cert_path)

    @staticmethod
    async def xor_cert(certify_key, input_file, output_file):
        xor_file(input_file=input_file,
                 output_file=output_file,
                 key=[ord(elem) for v in certify_key.values() for elem in v])
