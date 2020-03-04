import base64
import hashlib
import logging
import textwrap

from aiohttp import web
from aiohttp_jinja2 import template
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from app.service.auth_svc import check_authorization
from app.utility.base_service import BaseService
from app.utility.payload_encoder import xor_file


class TrainingApi(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.services = services
        self.certify_key = dict()

    @check_authorization
    @template('training.html')
    async def splash(self, request):
        return dict()

    @check_authorization
    async def retrieve_flags(self, request):
        flags = [flag for c in await self.data_svc.locate('certification') for flag in c.flags]
        for flag in flags:
            try:
                if not flag.completed:
                    if await flag.verify(self.services):
                        flag.completed = True
                        await self._A(flag)
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(flags=[f.display for f in flags]))

    @check_authorization
    async def generate_certificate(self, request):
        data = await request.json()
        if len(self.certify_key) == 30 and data.get('name'):
            name, payload = await self._build_certificate(name=data.get('name'))
            data = dict(img=base64.encodebytes(payload).decode('utf-8'))
            return web.json_response(data)
        return web.json_response(dict())

    async def load_key_for_existing_solves(self):
        flags = [flag for c in await self.data_svc.locate('certification') for flag in c.flags]
        for flag in flags:
            if flag.completed:
                await self._A(flag)

    async def decode_cert(self):
        xor_file(input_file='plugins/training/static/img/cert-img.encoded',
                 output_file='plugins/training/static/img/cert-img.decoded.jpg',
                 key=[ord(elem) for v in self.certify_key.values() for elem in v])

    async def encode_cert(self):
        xor_file(output_file='plugins/training/static/img/cert-img.encoded',
                 input_file='plugins/training/static/img/cert-img.decoded.jpg',
                 key=[ord(elem) for v in self.certify_key.values() for elem in v])

    """ PRIVATE """

    async def _A(self, f):
        F=ord;E=len;self.certify_key[f.number] = await self._B(f,E,F)

    async def _B(self, f, E, F):
        G=f.challenge.encode();R=base64.standard_b64encode;Q=f.completed;A=R(G);q=hashlib.sha256;B=q(A).hexdigest();B='%s'%B;A=A.decode('utf-8');C=E(A);D=E(B)
        if C>D:B=await self._C(B,C-D)
        elif D>C:A=await self._C(A,D-C)
        H=''.join([chr(F(C)^F(D))for(C,D)in zip(B,A)]);
        if Q:return '%s'%q(R(H.encode())).hexdigest()
        else:return await self._C('%s'%q(R(H.encode())).hexdigest(),15)

    @staticmethod
    async def _C(s, a):
        return s + ''.join(['0' for A in range(a)])

    async def _build_certificate(self, name):
        buff = xor_file(input_file='plugins/training/static/img/cert-img.encoded',
                        key=[ord(elem) for v in self.certify_key.values() for elem in v])
        return await self._populate_cert(name, buff)

    async def _populate_cert(self, name, buff):
        return await self.services.get('file_svc').read_file(name=await self._draw_name_on_cert(buff=buff,
                                                                                                name=await self._wrap_name_text(name)),
                                                             location='plugins/training/data/certificates/')

    @staticmethod
    async def _wrap_name_text(name):
        return '\n'.join(textwrap.TextWrapper(width=16).wrap(text=name))

    @staticmethod
    async def _draw_name_on_cert(buff, name):
        im = Image.open(BytesIO(buff))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('Verdana.ttf', 96)
        draw.text((550, 600), name, font=font, fill='white')
        save_name = '%s - Certificate.jpg' % name
        im.save('plugins/training/data/certificates/%s' % save_name)
        return save_name

