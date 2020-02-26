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
        return dict()

    @check_authorization
    async def retrieve_flags(self, request):
        flags = [flag for c in await self.data_svc.locate('certification') for flag in c.flags]
        for flag in flags:
            try:
                if not flag.completed:
                    if await flag.verify(self.services):
                        flag.completed = True
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(flags=[f.display for f in flags]))
