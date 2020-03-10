from hashlib import sha256
from importlib import import_module
from socket import gethostname

from app.utility.base_service import BaseService
from plugins.training.app.obfuscator import A


class TrainingService(BaseService):

    def __init__(self, services):
        self.log = self.add_service('training_svc', self)
        self.data_svc = services.get('data_svc')
        self.certify_key = dict()

    async def load_key_for_existing_solves(self):
        _, _, certifications = await self.get_all_flags_and_badges()
        for cert in certifications:
            self.certify_key[cert.name] = dict()
            for badge in cert.badges:
                for flag in badge.flags:
                    if flag.completed:
                        await self._check_valid_load(badge=badge, flag=flag, certification=cert.name)

    async def get_all_flags_and_badges(self, data=None):
        certifications = await self.data_svc.locate('certifications', data)
        badges = [badge for c in certifications for badge in c.badges]
        return [flag for b in badges for flag in b.flags], badges, certifications

    async def update_key(self, badge, flag):
        await self._check_valid_load(badge, flag)

    async def generate_proof(self, certification_name):
        if len(self.certify_key[certification_name]) == await self._get_flag_count_in_cert(certification_name):
            host = gethostname()
            return dict(hash=sha256(host.join([k for k in self.certify_key[certification_name].values()]).encode()).hexdigest(),
                        hostname=host)
        return dict()

    """ PRIVATE """

    async def _get_flag_count_in_cert(self, certification):
        flags, _, _ = await self.get_all_flags_and_badges(data=dict(name=certification))
        return len(flags)

    async def _check_valid_load(self, certification, badge, flag):
        cls = getattr(import_module('plugins.training.app.c_flag'), 'Flag')
        self.certify_key[certification]['%s-%s' % (badge.name, flag.number)] = await A(flag, cls)
