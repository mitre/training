import logging

from aiohttp import web
from aiohttp_jinja2 import template

from app.service.auth_svc import check_authorization
from app.utility.base_service import BaseService


class TrainingApi(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.services = services

    @check_authorization
    @template('training.html')
    async def splash(self, request):
        return dict(certificates=[cert.display for cert in await self.data_svc.locate('certifications')])

    @check_authorization
    async def retrieve_flags(self, request):
        data = dict(await request.json())
        badges = [badge for c in await self.data_svc.locate('certifications', data) for badge in c.badges]
        for flag in [flag for b in badges for flag in b.flags]:
            try:
                if not flag.completed:
                    if await flag.verify(self.services):
                        flag.completed = True
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(badges=[b.display for b in badges]))
