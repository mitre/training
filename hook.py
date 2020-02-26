from importlib import import_module

from app.utility.base_world import BaseWorld
from plugins.training.app.c_certification import Certification
from plugins.training.app.c_flag import Flag
from plugins.training.app.training_api import TrainingApi

name = 'Training'
description = 'A certification course to become a CALDERA SME'
address = '/plugin/training/gui'


async def enable(services):
    data_svc = services.get('data_svc')
    await data_svc.apply('certification')
    await _load_flags(data_svc)

    training_api = TrainingApi(services)
    app = services.get('app_svc').application
    app.router.add_static('/training', 'plugins/training/static/', append_version=True)
    app.router.add_route('GET', '/plugin/training/gui', training_api.splash)
    app.router.add_route('POST', '/plugin/training/flags', training_api.retrieve_flags)


async def _load_flags(data_svc):
    cert = BaseWorld.strip_yml('plugins/training/data/9cd5f3a0-765d-45bc-85c2-bc76d4282599.yml')[0]
    certification = Certification(name=cert['name'])
    for number, module in cert['flags'].items():
        loaded_module = import_module('plugins.training.%s' % module)
        certification.flags.append(Flag(verify=getattr(loaded_module, 'verify'),
                                        number=number,
                                        name=getattr(loaded_module, 'name'),
                                        challenge=getattr(loaded_module, 'challenge')))
    await data_svc.store(certification)
