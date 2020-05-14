import logging

from aiohttp import web
from aiohttp_jinja2 import template

from app.utility.base_service import BaseService
from app.service.auth_svc import for_all_public_methods, check_authorization


@for_all_public_methods(check_authorization)
class TrainingApi(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.services = services

    @template('training.html')
    async def splash(self, request):
        access = dict(access=tuple(await self.auth_svc.get_permissions(request)))
        certifications = await self.data_svc.locate('certifications', match=access)
        return dict(certificates=[cert.display for cert in certifications])

    async def retrieve_flags(self, request):
        data = dict(await request.json())
        badges = [badge for c in await self.data_svc.locate('certifications', data) for badge in c.badges]
        for flag in [flag for b in badges for flag in b.flags]:
            try:
                if not flag.completed:
                    if await flag.activate(self.services):
                        flag.completed = await flag.verify(self.services, flag.setup_fields) if flag.setup_fields else \
                            await flag.verify(self.services)
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(badges=[b.display for b in badges]))
