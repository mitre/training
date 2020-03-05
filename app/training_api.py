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
        self._encoded_cert_path = 'plugins/training/static/img/cert-img.encoded'
        self._decoded_cert_path = 'plugins/training/static/img/cert-img.decoded.jpg'
        self._text = dict(font='Verdana.ttf', size=96, color='white', max_textbox_char_len=16)

    @check_authorization
    @template('training.html')
    async def splash(self, request):
        return dict()

    @check_authorization
    async def retrieve_flags(self, request):
        flags = await self._get_all_flags()
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
        flags = await self._get_all_flags()
        if len(self.certify_key) == len(flags) and data.get('name'):
            payload = await self._build_certificate(name=data.get('name'))
            return web.json_response(dict(img=base64.encodebytes(payload).decode('utf-8')))
        return web.json_response(dict())

    async def load_key_for_existing_solves(self):
        flags = await self._get_all_flags()
        for flag in flags:
            if flag.completed:
                await self._A(flag)

    async def decode_cert(self):
        await self._xor_cert(input_file=self._encoded_cert_path,
                             output_file=self._decoded_cert_path)

    async def encode_cert(self):
        await self._xor_cert(input_file=self._decoded_cert_path,
                             output_file=self._encoded_cert_path)

    """ PRIVATE """

    async def _get_all_flags(self):
        return [flag for c in await self.data_svc.locate('certification') for flag in c.flags]

    async def _xor_cert(self, input_file, output_file):
        xor_file(input_file=input_file,
                 output_file=output_file,
                 key=[ord(elem) for v in self.certify_key.values() for elem in v])

    async def _build_certificate(self, name):
        buff = xor_file(input_file=self._encoded_cert_path,
                        key=[ord(elem) for v in self.certify_key.values() for elem in v])
        return await self._populate_cert(name, buff)

    async def _populate_cert(self, name, buff):
        return await self._draw_name_on_cert(buff=buff, name=await self._wrap_name_text(name))

    async def _wrap_name_text(self, name):
        return '\n'.join(textwrap.TextWrapper(width=self._text['max_textbox_char_len']).wrap(text=name))

    async def _draw_name_on_cert(self, buff, name):
        try:
            im = Image.open(BytesIO(buff))
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(self._text['font'], self._text['size'])
            draw.text((550, 600), name, font=font, fill=self._text['color'])
            out_buff = BytesIO()
            im.save(out_buff, format='JPEG')
            return out_buff.getvalue()
        except Exception as e:
            print(e)

    """ DEOBFUSCATION FUNCTIONS """

    async def _A(self, f):
        F=ord;E=len;self.certify_key[f.number] = await self._B(f,E,F)

    async def _B(self, f, E, F):
        R=base64.standard_b64encode;q=hashlib.sha256;G=f.challenge.encode();A=R(G);B=q(A).hexdigest();B='%s'%B;Q=f.completed;A=A.decode('utf-8');C=E(A);D=E(B)
        if C>D:B=await self._C(B,C-D)
        elif D>C:A=await self._C(A,D-C)
        H=''.join([chr(F(C)^F(D))for(C,D)in zip(B,A)]);
        if Q:return '%s'%q(R(H.encode())).hexdigest()
        else:return await self._C('%s'%q(R(H.encode())).hexdigest(),15)

    @staticmethod
    async def _C(s, a):
        return s + ''.join(['0' for A in range(a)])

