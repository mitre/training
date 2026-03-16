"""Exhaustive tests for app.certificate_svc.CertificateService."""
import os
import json
import uuid
import pytest
import tempfile
from unittest.mock import patch, MagicMock

from plugins.training.app.certificate_svc import (
    CertificateService, _ensure_dirs, _load_index, _save_index,
    _load_or_create_secret, SECRET_FILE, OUT_DIR, INDEX_FILE,
)


@pytest.fixture
def tmp_dirs(tmp_path, monkeypatch):
    """Redirect all certificate_svc paths to a temp directory."""
    secret_file = str(tmp_path / '.secret')
    out_dir = str(tmp_path / 'generated_certificates')
    index_file = os.path.join(out_dir, 'issued.json')
    template_bg = str(tmp_path / 'static' / 'templates' / 'caldera_cert.png')

    monkeypatch.setattr('plugins.training.app.certificate_svc.SECRET_FILE', secret_file)
    monkeypatch.setattr('plugins.training.app.certificate_svc.OUT_DIR', out_dir)
    monkeypatch.setattr('plugins.training.app.certificate_svc.INDEX_FILE', index_file)
    monkeypatch.setattr('plugins.training.app.certificate_svc.TEMPLATE_BG_PNG', template_bg)
    monkeypatch.setattr('plugins.training.app.certificate_svc.LOGO_TOP_CENTER', str(tmp_path / 'logo1.png'))
    monkeypatch.setattr('plugins.training.app.certificate_svc.LOGO_BOTTOM_LEFT', str(tmp_path / 'logo2.png'))

    return dict(secret_file=secret_file, out_dir=out_dir, index_file=index_file)


class TestEnsureDirs:
    def test_creates_out_dir(self, tmp_dirs):
        _ensure_dirs()
        assert os.path.isdir(tmp_dirs['out_dir'])


class TestLoadOrCreateSecret:
    def test_creates_secret(self, tmp_dirs):
        secret = _load_or_create_secret()
        assert len(secret) == 16  # uuid4 bytes
        assert os.path.exists(tmp_dirs['secret_file'])

    def test_returns_same_secret(self, tmp_dirs):
        s1 = _load_or_create_secret()
        s2 = _load_or_create_secret()
        assert s1 == s2


class TestLoadSaveIndex:
    def test_empty_index(self, tmp_dirs):
        idx = _load_index()
        assert idx == {}

    def test_save_and_load(self, tmp_dirs):
        _ensure_dirs()
        _save_index({'key': {'path': '/foo', 'name': 'bar'}})
        idx = _load_index()
        assert 'key' in idx
        assert idx['key']['path'] == '/foo'


class TestCertificateService:
    def test_init(self, tmp_dirs):
        svc = CertificateService()
        assert svc.secret is not None
        assert len(svc.instance_id) == 12

    def test_key_format(self, tmp_dirs):
        svc = CertificateService()
        key = svc._key('user1', 'cert1')
        assert 'user1' in key
        assert 'cert1' in key
        assert svc.instance_id in key

    def test_already_issued_false(self, tmp_dirs):
        svc = CertificateService()
        assert svc.already_issued('u1', 'c1') is False

    def test_mark_and_already_issued(self, tmp_dirs):
        svc = CertificateService()
        svc.mark_issued('u1', 'c1', '/path/to/cert.pdf', 'Jane')
        assert svc.already_issued('u1', 'c1') is True

    def test_get_record(self, tmp_dirs):
        svc = CertificateService()
        svc.mark_issued('u1', 'c1', '/path/cert.pdf', 'Jane')
        rec = svc.get_record('u1', 'c1')
        assert rec is not None
        assert rec['path'] == '/path/cert.pdf'
        assert rec['name'] == 'Jane'
        assert 'issued_at' in rec

    def test_get_record_missing(self, tmp_dirs):
        svc = CertificateService()
        assert svc.get_record('u1', 'c1') is None

    def test_clear_issued(self, tmp_dirs):
        svc = CertificateService()
        svc.mark_issued('u1', 'c1', '/path', 'Jane')
        svc.clear_issued_for_user_cert('u1', 'c1')
        assert svc.already_issued('u1', 'c1') is False

    def test_clear_nonexistent_is_noop(self, tmp_dirs):
        svc = CertificateService()
        svc.clear_issued_for_user_cert('u1', 'c1')  # should not raise


class TestSignedToken:
    def test_sign_and_verify(self, tmp_dirs):
        svc = CertificateService()
        token = svc.signed_token('/some/path.pdf')
        result = svc.verify_token(token)
        assert result == '/some/path.pdf'

    def test_tampered_token(self, tmp_dirs):
        svc = CertificateService()
        token = svc.signed_token('/some/path.pdf')
        tampered = token[:-1] + ('a' if token[-1] != 'a' else 'b')
        assert svc.verify_token(tampered) is None

    def test_invalid_token_no_dot(self, tmp_dirs):
        svc = CertificateService()
        assert svc.verify_token('nodothere') is None

    def test_empty_token(self, tmp_dirs):
        svc = CertificateService()
        assert svc.verify_token('') is None

    def test_empty_payload(self, tmp_dirs):
        svc = CertificateService()
        token = svc.signed_token('')
        assert svc.verify_token(token) == ''


class TestSafePart:
    def test_simple_name(self, tmp_dirs):
        svc = CertificateService()
        assert svc._safe_part('Jane Doe') == 'Jane_Doe'

    def test_special_chars(self, tmp_dirs):
        svc = CertificateService()
        result = svc._safe_part('Jane@Doe!#$')
        assert '@' not in result
        assert '!' not in result

    def test_empty_string(self, tmp_dirs):
        svc = CertificateService()
        assert svc._safe_part('') == 'User'

    def test_whitespace_only(self, tmp_dirs):
        svc = CertificateService()
        assert svc._safe_part('   ') == 'User'

    def test_multiple_spaces(self, tmp_dirs):
        svc = CertificateService()
        assert svc._safe_part('Jane   Doe') == 'Jane_Doe'

    def test_preserves_dots_hyphens(self, tmp_dirs):
        svc = CertificateService()
        result = svc._safe_part('Jane-Doe.Jr')
        assert 'Jane-Doe.Jr' == result


class TestIssue:
    def test_issue_returns_path(self, tmp_dirs):
        svc = CertificateService()
        # Mock _build_pdf to avoid reportlab dependency
        svc._build_pdf = MagicMock()
        path = svc.issue('u1', 'Caldera User', 'Jane Doe')
        assert path.endswith('.pdf')
        assert 'Jane_Doe' in path

    def test_issue_filename_format(self, tmp_dirs):
        svc = CertificateService()
        svc._build_pdf = MagicMock()
        path = svc.issue('u1', 'Cert', 'John Smith')
        basename = os.path.basename(path)
        assert basename.startswith('Caldera_User_Certificate_')
        assert 'John_Smith' in basename


class TestDrawImageKeepAspect:
    def test_no_file_noop(self, tmp_dirs):
        svc = CertificateService()
        c = MagicMock()
        svc._draw_image_keep_aspect(c, '/nonexistent.png', 0, 0, target_w=100)
        c.drawImage.assert_not_called()
