"""Shared fixtures for the training plugin test suite."""
import os
import json
import sys
import types
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch, PropertyMock

# ---------------------------------------------------------------------------
# Stub out heavy / unavailable third-party imports *before* any app code
# ---------------------------------------------------------------------------

# reportlab stubs
for mod_name in (
    'reportlab', 'reportlab.lib', 'reportlab.lib.pagesizes', 'reportlab.pdfgen',
    'reportlab.lib.utils', 'reportlab.pdfbase', 'reportlab.pdfbase.ttfonts',
    'reportlab.lib.colors', 'reportlab.pdfgen.canvas',
):
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

# markdown stub
if 'markdown' not in sys.modules:
    _md = types.ModuleType('markdown')
    _md.markdown = lambda text: f'<p>{text}</p>'
    sys.modules['markdown'] = _md

# Minimal stubs for Caldera framework classes
_base_object_mod = types.ModuleType('app.utility.base_object')

class _BaseObject:
    def __init__(self):
        pass
    def hash(self, s):
        import hashlib
        return hashlib.md5(s.encode()).hexdigest()
    def retrieve(self, collection, unique):
        for item in collection:
            if getattr(item, 'unique', None) == unique:
                return item
        return None

_base_object_mod.BaseObject = _BaseObject
sys.modules['app'] = types.ModuleType('app')
sys.modules['app.utility'] = types.ModuleType('app.utility')
sys.modules['app.utility.base_object'] = _base_object_mod

def _verify_hash(hash_val, target):
    return False


_config_util_mod = types.ModuleType('app.utility.config_util')
_config_util_mod.verify_hash = _verify_hash
sys.modules['app.utility.config_util'] = _config_util_mod

_base_world_mod = types.ModuleType('app.utility.base_world')

class _Access:
    APP = 'app'
    RED = 'red'
    BLUE = 'blue'
    HIDDEN = 'hidden'

class _BaseWorld:
    Access = _Access
    @staticmethod
    def get_config(name=None, prop=None):
        return None
    @staticmethod
    def strip_yml(filename):
        return []

_base_world_mod.BaseWorld = _BaseWorld
sys.modules['app.utility.base_world'] = _base_world_mod

_base_svc_mod = types.ModuleType('app.utility.base_service')
class _BaseService:
    pass
_base_svc_mod.BaseService = _BaseService
sys.modules['app.utility.base_service'] = _base_svc_mod

_auth_svc_mod = types.ModuleType('app.service.auth_svc')
def _for_all(decorator):
    def wrapper(cls):
        return cls
    return wrapper
_auth_svc_mod.for_all_public_methods = _for_all
_auth_svc_mod.check_authorization = lambda f: f
sys.modules['app.service'] = types.ModuleType('app.service')
sys.modules['app.service.auth_svc'] = _auth_svc_mod

# aiohttp / jinja stubs
_aiohttp_mod = types.ModuleType('aiohttp')
class _WebModule:
    class HTTPNotFound(Exception):
        def __init__(self, text=''):
            self.text = text
            super().__init__(text)
    class HTTPBadRequest(Exception):
        def __init__(self, text=''):
            self.text = text
            super().__init__(text)
    class HTTPForbidden(Exception):
        def __init__(self, text=''):
            self.text = text
            super().__init__(text)
    class HTTPInternalServerError(Exception):
        def __init__(self, text=''):
            self.text = text
            super().__init__(text)
    HTTPException = Exception
    @staticmethod
    def json_response(data):
        return data
    class FileResponse:
        def __init__(self, path, headers=None):
            self.path = path
            self.headers = headers
_aiohttp_mod.web = _WebModule
sys.modules['aiohttp'] = _aiohttp_mod
sys.modules['aiohttp.web'] = _aiohttp_mod.web  # needed for 'from aiohttp import web'

_jinja_mod = types.ModuleType('aiohttp_jinja2')
def _template(name):
    def decorator(func):
        return func
    return decorator
_jinja_mod.template = _template
sys.modules['aiohttp_jinja2'] = _jinja_mod

# ---------------------------------------------------------------------------
# Make plugin importable as plugins.training.*
# ---------------------------------------------------------------------------
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.dirname(PLUGIN_ROOT)

# Ensure plugins.training points to this repo
if 'plugins' not in sys.modules:
    plugins_mod = types.ModuleType('plugins')
    plugins_mod.__path__ = [PLUGINS_DIR]
    sys.modules['plugins'] = plugins_mod

training_pkg = types.ModuleType('plugins.training')
training_pkg.__path__ = [PLUGIN_ROOT]
training_pkg.__file__ = os.path.join(PLUGIN_ROOT, '__init__.py')
training_pkg.PLUGIN_DIR = PLUGIN_ROOT
sys.modules['plugins.training'] = training_pkg

# Also set as attribute on plugins module so `import plugins.training` works
sys.modules['plugins'].training = training_pkg

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

from plugins.training.app.c_flag import Flag
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_certification import Certification
from plugins.training.app.c_exam import Exam
from plugins.training.app import errors


class FakeFlag(Flag):
    """Concrete Flag subclass for testing."""
    name = 'Fake Flag'
    challenge = 'Do the thing'
    extra_info = 'Extra'

    async def verify(self, services):
        return True


class CompletedFlag(Flag):
    """A flag that starts completed."""
    name = 'Completed Flag'
    challenge = 'Already done'
    extra_info = ''

    def __init__(self, number):
        super().__init__(number)
        self.completed = True

    async def verify(self, services):
        return True


class ResettableFlag(Flag):
    """A flag with additional_fields that make it resettable."""
    name = 'Resettable Flag'
    challenge = 'Reset me'
    extra_info = ''
    additional_fields = dict(adversary_id='abc', operation_name='test_op')

    async def verify(self, services):
        return True


class FailFlag(Flag):
    """A flag whose verify always fails."""
    name = 'Fail Flag'
    challenge = 'Cannot pass'
    extra_info = ''

    async def verify(self, services):
        return False


@pytest.fixture
def fake_flag():
    return FakeFlag(number=1)


@pytest.fixture
def completed_flag():
    return CompletedFlag(number=2)


@pytest.fixture
def resettable_flag():
    return ResettableFlag(number=3)


@pytest.fixture
def fail_flag():
    return FailFlag(number=4)


@pytest.fixture
def badge_with_flags():
    b = Badge(name='test-badge')
    b.flags = [FakeFlag(number=1), FakeFlag(number=2)]
    return b


@pytest.fixture
def certification_with_badges():
    cert = Certification(
        identifier='cert-1',
        name='Test Cert',
        description='A test certification',
        access=_Access.RED,
    )
    b1 = Badge(name='badge-1')
    b1.flags = [FakeFlag(number=1)]
    b2 = Badge(name='badge-2')
    b2.flags = [FakeFlag(number=2)]
    cert.badges = [b1, b2]
    return cert


@pytest.fixture
def exam_with_badges():
    exam = Exam(
        identifier='exam-1',
        name='Test Exam',
        description='An exam certification',
        access=_Access.APP,
    )
    b = Badge(name='exam-badge')
    b.flags = [FakeFlag(number=1)]
    exam.badges = [b]
    return exam


@pytest.fixture
def mock_services():
    """Return a dict-like services mock matching Caldera's service registry."""
    services = {}
    data_svc = AsyncMock()
    data_svc.locate = AsyncMock(return_value=[])
    auth_svc = MagicMock()
    auth_svc.get_permissions = AsyncMock(return_value=[])
    auth_svc.bypass = []
    auth_svc.user_map = {}
    rest_svc = AsyncMock()
    app_svc = MagicMock()
    app_svc.get_config = MagicMock(return_value=None)
    contact_svc = MagicMock()
    contact_svc.report = {'websocket': []}
    file_svc = AsyncMock()

    services['data_svc'] = data_svc
    services['auth_svc'] = auth_svc
    services['rest_svc'] = rest_svc
    services['app_svc'] = app_svc
    services['contact_svc'] = contact_svc
    services['file_svc'] = file_svc

    class ServiceDict(dict):
        pass

    sd = ServiceDict(services)
    return sd
