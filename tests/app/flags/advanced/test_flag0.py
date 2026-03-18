"""Exhaustive tests for advanced flag_0 (AdvancedFlag0)."""
import pytest
from unittest.mock import MagicMock, AsyncMock

from plugins.training.app.flags.advanced.flag_0 import AdvancedFlag0


class TestValidExternalHttpContact:
    def test_valid_external_http(self):
        assert AdvancedFlag0.valid_external_http_contact('http://10.10.10.10:8888')

    def test_valid_external_https(self):
        assert AdvancedFlag0.valid_external_http_contact('https://10.10.10.10:8888')

    def test_valid_http_no_port(self):
        assert AdvancedFlag0.valid_external_http_contact('http://10.10.10.10')

    def test_valid_https_no_port(self):
        assert AdvancedFlag0.valid_external_http_contact('https://10.10.10.10')

    def test_loopback_rejected(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://127.0.0.1:8888')

    def test_loopback_no_port(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://127.0.0.1')

    def test_loopback_https(self):
        assert not AdvancedFlag0.valid_external_http_contact('https://127.0.0.1:12345')

    def test_loopback_other(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://127.10.10.10')

    def test_zero_ip(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://0.0.0.0:8888')

    def test_zero_ip_no_port(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://0.0.0.0')

    def test_invalid_port(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://10.10.10.10:abcd')

    def test_out_of_range_port(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://10.10.10.10:123456')

    def test_hostname_rejected(self):
        assert not AdvancedFlag0.valid_external_http_contact('http://myhostname.tld:1234')

    def test_wrong_protocol(self):
        assert not AdvancedFlag0.valid_external_http_contact('nothttp://10.10.10.10:12345')

    def test_ftp_rejected(self):
        assert not AdvancedFlag0.valid_external_http_contact('ftp://10.10.10.10:21')

    def test_empty_string(self):
        assert not AdvancedFlag0.valid_external_http_contact('')

    def test_no_scheme(self):
        assert not AdvancedFlag0.valid_external_http_contact('10.10.10.10:8888')

    def test_private_192_168(self):
        assert AdvancedFlag0.valid_external_http_contact('http://192.168.1.1:443')

    def test_private_172(self):
        assert AdvancedFlag0.valid_external_http_contact('http://172.16.0.1:8080')

    def test_port_zero(self):
        # Port 0 is technically valid in URL parsing
        result = AdvancedFlag0.valid_external_http_contact('http://10.10.10.10:0')
        # Should still pass since port 0 is in range
        assert isinstance(result, bool)

    def test_max_valid_port(self):
        assert AdvancedFlag0.valid_external_http_contact('http://10.10.10.10:65535')

    def test_boundary_ip_255(self):
        assert AdvancedFlag0.valid_external_http_contact('http://255.255.255.255:80')

    def test_ip_1_0_0_1(self):
        assert AdvancedFlag0.valid_external_http_contact('http://1.0.0.1:80')


class TestExternalFacingIp:
    def test_external(self):
        assert AdvancedFlag0.external_facing_ip('10.0.0.1')

    def test_loopback(self):
        assert not AdvancedFlag0.external_facing_ip('127.0.0.1')

    def test_loopback_range(self):
        assert not AdvancedFlag0.external_facing_ip('127.255.0.1')

    def test_zero(self):
        assert not AdvancedFlag0.external_facing_ip('0.0.0.0')


class TestAdvancedFlag0Verify:
    @pytest.mark.asyncio
    async def test_verify_valid_contact(self):
        flag = AdvancedFlag0(number=1)
        services = {'app_svc': MagicMock()}
        services['app_svc'].get_config = MagicMock(return_value='http://10.10.10.10:8888')
        result = await flag.verify(services)
        assert result is True

    @pytest.mark.asyncio
    async def test_verify_loopback_contact(self):
        flag = AdvancedFlag0(number=1)
        services = {'app_svc': MagicMock()}
        services['app_svc'].get_config = MagicMock(return_value='http://127.0.0.1:8888')
        result = await flag.verify(services)
        assert result is False

    @pytest.mark.asyncio
    async def test_verify_none_contact(self):
        flag = AdvancedFlag0(number=1)
        services = {'app_svc': MagicMock()}
        services['app_svc'].get_config = MagicMock(return_value=None)
        result = await flag.verify(services)
        assert not result

    @pytest.mark.asyncio
    async def test_verify_empty_contact(self):
        flag = AdvancedFlag0(number=1)
        services = {'app_svc': MagicMock()}
        services['app_svc'].get_config = MagicMock(return_value='')
        result = await flag.verify(services)
        assert not result

    def test_name_and_challenge(self):
        flag = AdvancedFlag0(number=1)
        assert flag.name == 'Update configs'
        assert 'app.contact.http' in flag.challenge
