import logging
import traceback

import os, hashlib, mimetypes, base64

from aiohttp import web
from aiohttp_jinja2 import template

from app.utility.base_service import BaseService
from app.service.auth_svc import for_all_public_methods, check_authorization
from plugins.training.app import errors
from plugins.training.app.base_flag import BaseFlag
from plugins.training.app.certificate_svc import CertificateService


@for_all_public_methods(check_authorization)
class TrainingApi(BaseService):

    def __init__(self, services):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.services = services
        self.cert_service = CertificateService()
        self.logger = logging.getLogger('training_api')

    @template('training.html')
    async def splash(self, request):
        access = dict(access=tuple(await self.auth_svc.get_permissions(request)))
        certifications = await self.data_svc.locate('certifications', match=access)
        return dict(certificates=[cert.display for cert in certifications])

    @template('flag_solution_guide.html')
    async def flag_solution_guide(self, request):
        cert_name = request.match_info['cert_name']
        badge_name = request.match_info['badge_name']
        flag_name = request.match_info['flag_name']

        certificate_list = await self.data_svc.locate('certifications', match={'name': cert_name})

        if not certificate_list:
            raise web.HTTPNotFound(text='Certificate does not exist')

        certificate = certificate_list[0]

        try:
            flag = certificate.get_flag(badge_name, flag_name)
        except errors.BadgeDoesNotExist:
            raise web.HTTPNotFound(text='Badge does not exist')
        except errors.FlagDoesNotExist:
            raise web.HTTPNotFound(text='Flag does not exist')

        if not flag.has_solution_guide:
            raise web.HTTPNotFound(text='No solution guide exists for flag')

        return dict(flag=flag)

    @template('certificate_solution_guide.html')
    async def certificate_solution_guide(self, request):
        cert_name = request.match_info['cert_name']
        certificate_list = await self.data_svc.locate('certifications', match={'name': cert_name})

        if not certificate_list:
            raise web.HTTPNotFound(text='Certificate does not exist')

        return dict(certificate=certificate_list[0])

    def _request_user_id(self, request) -> str:
        # Stable per-user key: API KEY header or fallback
        return request.headers.get('X-User-ID') or request.headers.get('KEY') or 'unknown'
    
    async def retrieve_flags(self, request):
        data = dict(await request.json())
        answers = {}
        if 'answers' in data.keys():
            answers = data.pop('answers')
        cert = next(c for c in await self.data_svc.locate('certifications', data))
        badges = [badge for badge in cert.badges]
        for flag in [flag for b in badges for flag in b.flags]:
            try:
                if not flag.completed:
                    flag.activate()
                    if hasattr(flag, 'answer'):
                        answer = answers.get(str(flag.number), None)
                        if answer:
                            flag.completed = flag.verify(answer)
                    else:
                        flag.completed = await flag.verify(self.services)

            except Exception as e:
                logging.error(e)
        return web.json_response(dict(badges=[b.display for b in badges]))

    async def retrieve_certs(self, request):
        access = dict(access=tuple(await self.auth_svc.get_permissions(request)))
        certifications = await self.data_svc.locate('certifications', match=access)
        return web.json_response(dict(certificates=[cert.display for cert in certifications]))

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
                    if all(field in flag.additional_fields for field in ['adversary_id', 'operation_name']):
                        await BaseFlag.reset(self.services, flag.additional_fields['operation_name'], flag.verify)
                        reset = 1
                    break
            except Exception as e:
                logging.error(e)
        return web.json_response(dict(reset=reset))

    async def can_issue(self, request, cert_name):
        # Compute completion using same badge/flag iteration used in retrieve_flags
        access = dict(access=tuple(await self.auth_svc.get_permissions(request)))
        certs = await self.data_svc.locate('certifications', match=access)
        cert = next((c for c in certs if c.name == cert_name), None)
        if not cert:
            raise web.HTTPNotFound(text='Certificate does not exist')
        
        # Debugging bypass
        if os.getenv("TRAINING_CERT_BYPASS") == "1":
            return cert, True
    
        complete = all(f.completed for b in cert.badges for f in b.flags)
        return cert, complete
    
    async def issue_certificate(self, request):
        """
        POST /plugin/training/certificate/issue
        { "certificate": "Caldera User", "name": "Jane Doe" }
        """
        try:
            body = await request.json()
            cert_name = body.get('certificate')
            display_name = body.get('name')
            self.logger.debug("issue_certificate: body=%r", body)
            if not cert_name or not display_name:
                raise web.HTTPBadRequest(text='certificate and name required')

            user_id = self._request_user_id(request)
            self.logger.debug("issue_certificate: user_id=%s", user_id)

            cert, complete = await self.can_issue(request, cert_name)
            cert_id = getattr(cert, 'unique', None) or getattr(cert, 'identifier', None) or getattr(cert, 'id', None) or cert.name
            self.logger.debug("issue_certificate: cert_id=%s complete=%s", cert_id, complete)
            if not complete:
                raise web.HTTPForbidden(text='Training not complete')

            if self.cert_service.already_issued(user_id, cert_id):
                # Return existing (idempotent UX)
                rec = self.cert_service.get_record(user_id, cert_id)
                payload = rec['path']
                token = self.cert_service.signed_token(payload)
                return web.json_response({'alreadyIssued': True, 'download': f'/plugin/training/certificate/download?token={token}'})

            # Generate PDF directly
            path = self.cert_service.issue(user_id, cert.name, display_name)
            self.cert_service.mark_issued(user_id, cert_id, path, display_name)
            token = self.cert_service.signed_token(path)
            return web.json_response({'alreadyIssued': False, 'download': f'/plugin/training/certificate/download?token={token}'})
        except web.HTTPException:
            raise
        except Exception as e:
            logging.exception("issue_certificate failed: {}".format(e))
            raise web.HTTPInternalServerError(text='issue_certificate failed; see server logs')

    async def reset_issuance(self, request):
        """
        POST /plugin/training/certificate/reset
        { "certificate": "Caldera User", "user_id": "<optional override>" }
        Called by existing reset logic after training reset completes.
        """
        body = await request.json()
        cert_name = body.get('certificate')
        if not cert_name:
            raise web.HTTPBadRequest(text='certificate required')
        user_id = body.get('user_id') or self._request_user_id(request)

        # Map cert_name to unique id
        certs = await self.data_svc.locate('certifications', {})
        cert = next((c for c in certs if c.name == cert_name), None)
        if not cert:
            raise web.HTTPNotFound(text='Certificate does not exist')
        cert_id = getattr(cert, 'unique', None) or getattr(cert, 'identifier', None) or getattr(cert, 'id', None) or cert.name
        self.cert_service.clear_issued_for_user_cert(user_id, cert_id)
        return web.json_response({'ok': True})
    
    def _attachment_headers(self, filename: str) -> dict:
        ctype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        return {
            'Content-Type': ctype,
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
    async def download_certificate(self, request):
        token = request.query.get('token', '')
        path = self.cert_service.verify_token(token)
        if not path or not os.path.exists(path):
            raise web.HTTPNotFound(text='Invalid or expired token')

        # pick a good filename (using existing generator logic)
        filename = os.path.basename(path)
        return web.FileResponse(path, headers=self._attachment_headers(filename))
    
    async def issue_certificate_bytes(self, request):
        """
        POST /plugin/training/certificate/issue-bytes
        { "certificate": "User Certificate", "name": "Jane Doe" }
        -> { "filename": "Caldera_User_Certificate_Jane_Doe_20250928.pdf",
             "pdf_bytes": "<base64>" }
        """
        body = await request.json()
        cert_name = body.get('certificate')
        display_name = body.get('name')
        if not cert_name or not display_name:
            raise web.HTTPBadRequest(text='certificate and name required')

        user_id = self._request_user_id(request)
        cert, complete = await self.can_issue(request, cert_name)
        cert_id = getattr(cert, 'unique', None) or getattr(cert, 'identifier', None) or getattr(cert, 'id', None) or cert.name
        if not complete:
            raise web.HTTPForbidden(text='Training not complete')

        # generate fresh PDF (no caching; you can add idempotence if you want)
        pdf_path = self.cert_service.issue(user_id, cert.name, display_name)

        # remember issuance like before
        self.cert_service.mark_issued(user_id, cert_id, pdf_path, display_name)

        # return filename + bytes (Debrief style)
        with open(pdf_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')

        return web.json_response({
            'filename': os.path.basename(pdf_path),
            'pdf_bytes': b64
        })
