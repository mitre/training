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
        complete = await self.data_svc.locate('flags', dict(completed=True))
        for incomplete in sorted(await self.data_svc.locate('flags', dict(completed=False)), key=lambda x: x.number):
            try:
                verified = await incomplete.verify(self.services)
                if verified:
                    incomplete.completed = True
                    complete.append(incomplete)
                else:
                    complete.append(incomplete)
                    break
            except Exception as e:
                print(e)
        return web.json_response(dict(flags=[f.display for f in complete]))
