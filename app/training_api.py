import base64
import logging

from aiohttp import web
from aiohttp_jinja2 import template

from app.service.auth_svc import check_authorization
from app.utility.base_service import BaseService


class TrainingApi(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.training_svc = services.get('training_svc')
        self.services = services

    @check_authorization
    @template('training.html')
    async def splash(self, request):
        access = dict(access=tuple(await self.auth_svc.get_permissions(request)))
        certifications = await self.data_svc.locate('certifications', match=access)
        return dict(certificates=[cert.display for cert in certifications])

    @check_authorization
    async def retrieve_flags(self, request):
        data = dict(await request.json())
        flags, badges = await self.training_svc.get_all_flags_and_badges(data=data)
        for flag in flags:
            try:
                if not flag.completed:
                    if await flag.verify(self.services):
                        flag.completed = True
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(badges=[b.display for b in badges]))

    @check_authorization
    async def generate_certificate(self, request):
        data = await request.json()
        flags, _ = await self.training_svc.get_all_flags_and_badges()
        if len(self.training_svc.certify_key) == len(flags) and data.get('name') and data.get('certification'):
            payload = await self.training_svc.build_certificate(name=data.get('name'),
                                                                cert_name=data.get('certification'))
            return web.json_response(dict(img=base64.encodebytes(payload).decode('utf-8')))
        return web.json_response(dict())
