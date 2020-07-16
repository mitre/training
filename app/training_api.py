import logging

from aiohttp import web
from aiohttp_jinja2 import template

from app.utility.base_service import BaseService
from app.service.auth_svc import for_all_public_methods, check_authorization
from plugins.training.app.base_flag import BaseFlag


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
                    flag.activate()
                    if await flag.verify(self.services):
                        flag.completed = True
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(badges=[b.display for b in badges]))

    async def reset_flag(self, request):
        """
        Allows cert takers to reset the latest flag if something went wrong with running the automatic operation.
        We know a flag has a reset capability if it has a field called 'adversary_id'.
        """
        data = await request.json()
        badges = [badge for c in await self.data_svc.locate('certifications', data) for badge in c.badges]
        reset = 0
        for flag in [flag for b in badges for flag in b.flags]:
            try:
                if not flag.completed:
                    if hasattr(flag, 'adversary_id'):
                        await BaseFlag.reset(self.services, flag.operation_name)
                        reset = 1
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(reset=reset))