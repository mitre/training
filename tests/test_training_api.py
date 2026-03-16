"""Exhaustive tests for app.training_api.TrainingApi."""
import os
import json
import pytest
from unittest.mock import MagicMock, AsyncMock, patch, PropertyMock
from aiohttp import web

from plugins.training.app.training_api import TrainingApi
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_certification import Certification
from plugins.training.app.c_flag import Flag
from plugins.training.app import errors


class FakeFlag(Flag):
    name = 'FakeFlag'
    challenge = 'Test'
    extra_info = ''

    def __init__(self, number, completed=False):
        super().__init__(number)
        if completed:
            self.completed = True

    async def verify(self, services):
        return True


class AnswerFlag(Flag):
    """A flag with an answer attribute (fill-in-blank style)."""
    name = 'AnswerFlag'
    challenge = 'Answer it'
    extra_info = ''
    answer = 'correct'

    async def verify(self, services):
        # not used directly in retrieve_flags for answer-based flags
        return True

    def verify(self, answer):
        return answer.lower() == self.answer


def _make_services():
    services = {}
    data_svc = AsyncMock()
    data_svc.locate = AsyncMock(return_value=[])
    auth_svc = MagicMock()
    auth_svc.get_permissions = AsyncMock(return_value=[])
    services['data_svc'] = data_svc
    services['auth_svc'] = auth_svc
    return services


def _make_request(json_data=None, headers=None, match_info=None, query=None):
    request = MagicMock()
    request.json = AsyncMock(return_value=json_data or {})
    request.headers = headers or {}
    request.match_info = match_info or {}
    request.query = query or {}
    return request


def _make_cert(name='Test Cert', completed=False):
    cert = Certification(
        identifier='c1', name=name,
        description='desc', access='app'
    )
    b = Badge(name='badge-1')
    f = FakeFlag(number=1, completed=completed)
    b.flags.append(f)
    cert.badges.append(b)
    return cert


class TestTrainingApiInit:
    def test_init(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
            assert api.auth_svc is services['auth_svc']
            assert api.data_svc is services['data_svc']


class TestRequestUserId:
    def test_x_user_id_header(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(headers={'X-User-ID': 'user123'})
        assert api._request_user_id(request) == 'user123'

    def test_key_header_fallback(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(headers={'KEY': 'apikey'})
        assert api._request_user_id(request) == 'apikey'

    def test_unknown_fallback(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(headers={})
        assert api._request_user_id(request) == 'unknown'

    def test_x_user_id_takes_precedence(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(headers={'X-User-ID': 'uid', 'KEY': 'key'})
        assert api._request_user_id(request) == 'uid'


class TestSplash:
    @pytest.mark.asyncio
    async def test_splash_returns_certificates(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        result = await api.splash(request)
        assert 'certificates' in result
        assert len(result['certificates']) == 1


class TestRetrieveCerts:
    @pytest.mark.asyncio
    async def test_retrieve_certs(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        result = await api.retrieve_certs(request)
        assert 'certificates' in result
        assert len(result['certificates']) == 1


class TestRetrieveFlags:
    @pytest.mark.asyncio
    async def test_retrieve_flags_basic(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'name': 'Test Cert'})
        result = await api.retrieve_flags(request)
        assert 'badges' in result

    @pytest.mark.asyncio
    async def test_retrieve_flags_with_answers(self):
        services = _make_services()
        cert = Certification(identifier='c1', name='Test', description='d', access='app')
        b = Badge(name='b')
        af = AnswerFlag(number=1)
        b.flags.append(af)
        cert.badges.append(b)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'name': 'Test', 'answers': {'1': 'correct'}})
        result = await api.retrieve_flags(request)
        assert 'badges' in result


class TestResetFlag:
    @pytest.mark.asyncio
    async def test_reset_no_resettable_flags(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'name': 'Test Cert'})
        result = await api.reset_flag(request)
        assert result['reset'] == 0


class TestFlagSolutionGuide:
    @pytest.mark.asyncio
    async def test_cert_not_found(self):
        services = _make_services()
        services['data_svc'].locate = AsyncMock(return_value=[])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(match_info={
            'cert_name': 'Missing', 'badge_name': 'b', 'flag_name': 'f'
        })
        with pytest.raises(web.HTTPNotFound):
            await api.flag_solution_guide(request)

    @pytest.mark.asyncio
    async def test_badge_not_found(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(match_info={
            'cert_name': 'Test Cert', 'badge_name': 'nonexistent', 'flag_name': 'f'
        })
        with pytest.raises(web.HTTPNotFound):
            await api.flag_solution_guide(request)

    @pytest.mark.asyncio
    async def test_flag_not_found(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(match_info={
            'cert_name': 'Test Cert', 'badge_name': 'badge-1', 'flag_name': 'nonexistent'
        })
        with pytest.raises(web.HTTPNotFound):
            await api.flag_solution_guide(request)


class TestCertificateSolutionGuide:
    @pytest.mark.asyncio
    async def test_cert_not_found(self):
        services = _make_services()
        services['data_svc'].locate = AsyncMock(return_value=[])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(match_info={'cert_name': 'Missing'})
        with pytest.raises(web.HTTPNotFound):
            await api.certificate_solution_guide(request)

    @pytest.mark.asyncio
    async def test_cert_found(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(match_info={'cert_name': 'Test Cert'})
        result = await api.certificate_solution_guide(request)
        assert 'certificate' in result


class TestCanIssue:
    @pytest.mark.asyncio
    async def test_cert_not_found(self):
        services = _make_services()
        services['data_svc'].locate = AsyncMock(return_value=[])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        with pytest.raises(web.HTTPNotFound):
            await api.can_issue(request, 'Missing')

    @pytest.mark.asyncio
    async def test_incomplete(self):
        services = _make_services()
        cert = _make_cert(completed=False)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        _, complete = await api.can_issue(request, 'Test Cert')
        assert complete is False

    @pytest.mark.asyncio
    async def test_complete(self):
        services = _make_services()
        cert = _make_cert(completed=True)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        _, complete = await api.can_issue(request, 'Test Cert')
        assert complete is True

    @pytest.mark.asyncio
    async def test_bypass_env(self):
        services = _make_services()
        cert = _make_cert(completed=False)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request()
        with patch.dict(os.environ, {'TRAINING_CERT_BYPASS': '1'}):
            _, complete = await api.can_issue(request, 'Test Cert')
            assert complete is True


class TestIssueCertificate:
    @pytest.mark.asyncio
    async def test_missing_fields(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'certificate': 'Cert'})  # missing name
        with pytest.raises(web.HTTPBadRequest):
            await api.issue_certificate(request)

    @pytest.mark.asyncio
    async def test_not_complete(self):
        services = _make_services()
        cert = _make_cert(completed=False)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(
            json_data={'certificate': 'Test Cert', 'name': 'Jane'},
            headers={'X-User-ID': 'u1'}
        )
        with pytest.raises(web.HTTPForbidden):
            await api.issue_certificate(request)

    @pytest.mark.asyncio
    async def test_already_issued(self):
        services = _make_services()
        cert = _make_cert(completed=True)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        mock_cert_svc = MagicMock()
        mock_cert_svc.already_issued.return_value = True
        mock_cert_svc.get_record.return_value = {'path': '/cert.pdf'}
        mock_cert_svc.signed_token.return_value = '/cert.pdf.sig'
        with patch('plugins.training.app.training_api.CertificateService', return_value=mock_cert_svc):
            api = TrainingApi(services)
        request = _make_request(
            json_data={'certificate': 'Test Cert', 'name': 'Jane'},
            headers={'X-User-ID': 'u1'}
        )
        result = await api.issue_certificate(request)
        assert result['alreadyIssued'] is True

    @pytest.mark.asyncio
    async def test_new_issuance(self):
        services = _make_services()
        cert = _make_cert(completed=True)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        mock_cert_svc = MagicMock()
        mock_cert_svc.already_issued.return_value = False
        mock_cert_svc.issue.return_value = '/path/cert.pdf'
        mock_cert_svc.signed_token.return_value = '/path/cert.pdf.sig'
        with patch('plugins.training.app.training_api.CertificateService', return_value=mock_cert_svc):
            api = TrainingApi(services)
        request = _make_request(
            json_data={'certificate': 'Test Cert', 'name': 'Jane'},
            headers={'X-User-ID': 'u1'}
        )
        result = await api.issue_certificate(request)
        assert result['alreadyIssued'] is False
        assert 'download' in result


class TestResetIssuance:
    @pytest.mark.asyncio
    async def test_missing_cert_name(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={})
        with pytest.raises(web.HTTPBadRequest):
            await api.reset_issuance(request)

    @pytest.mark.asyncio
    async def test_cert_not_found(self):
        services = _make_services()
        services['data_svc'].locate = AsyncMock(return_value=[])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'certificate': 'Missing'})
        with pytest.raises(web.HTTPNotFound):
            await api.reset_issuance(request)

    @pytest.mark.asyncio
    async def test_successful_reset(self):
        services = _make_services()
        cert = _make_cert()
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        mock_cert_svc = MagicMock()
        with patch('plugins.training.app.training_api.CertificateService', return_value=mock_cert_svc):
            api = TrainingApi(services)
        request = _make_request(
            json_data={'certificate': 'Test Cert'},
            headers={'X-User-ID': 'u1'}
        )
        result = await api.reset_issuance(request)
        assert result['ok'] is True
        mock_cert_svc.clear_issued_for_user_cert.assert_called_once()


class TestDownloadCertificate:
    @pytest.mark.asyncio
    async def test_invalid_token(self):
        services = _make_services()
        mock_cert_svc = MagicMock()
        mock_cert_svc.verify_token.return_value = None
        with patch('plugins.training.app.training_api.CertificateService', return_value=mock_cert_svc):
            api = TrainingApi(services)
        request = _make_request(query={'token': 'bad'})
        with pytest.raises(web.HTTPNotFound):
            await api.download_certificate(request)

    @pytest.mark.asyncio
    async def test_missing_file(self):
        services = _make_services()
        mock_cert_svc = MagicMock()
        mock_cert_svc.verify_token.return_value = '/nonexistent.pdf'
        with patch('plugins.training.app.training_api.CertificateService', return_value=mock_cert_svc):
            api = TrainingApi(services)
        request = _make_request(query={'token': 'valid'})
        with pytest.raises(web.HTTPNotFound):
            await api.download_certificate(request)


class TestAttachmentHeaders:
    def test_pdf_content_type(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        headers = api._attachment_headers('cert.pdf')
        assert 'Content-Type' in headers
        assert 'Content-Disposition' in headers
        assert 'cert.pdf' in headers['Content-Disposition']

    def test_unknown_extension(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        headers = api._attachment_headers('file.qqqzzz')
        assert headers['Content-Type'] == 'application/octet-stream'


class TestIssueCertificateBytes:
    @pytest.mark.asyncio
    async def test_missing_fields(self):
        services = _make_services()
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(json_data={'certificate': 'C'})
        with pytest.raises(web.HTTPBadRequest):
            await api.issue_certificate_bytes(request)

    @pytest.mark.asyncio
    async def test_not_complete(self):
        services = _make_services()
        cert = _make_cert(completed=False)
        services['data_svc'].locate = AsyncMock(return_value=[cert])
        with patch('plugins.training.app.training_api.CertificateService'):
            api = TrainingApi(services)
        request = _make_request(
            json_data={'certificate': 'Test Cert', 'name': 'Jane'},
            headers={'X-User-ID': 'u1'}
        )
        with pytest.raises(web.HTTPForbidden):
            await api.issue_certificate_bytes(request)
