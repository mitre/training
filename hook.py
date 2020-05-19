import glob
from importlib import import_module

from app.utility.base_world import BaseWorld
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_certification import Certification
from plugins.training.app.c_flag import Flag
from plugins.training.app.training_api import TrainingApi

name = 'Training'
description = 'A certification course to become a CALDERA SME'
address = '/plugin/training/gui'


async def enable(services):
    data_svc = services.get('data_svc')
    await data_svc.apply('certifications')
    await _load_flags(data_svc)

    training_api = TrainingApi(services)
    app = services.get('app_svc').application
    app.router.add_static('/training', 'plugins/training/static/', append_version=True)
    app.router.add_route('GET', '/plugin/training/gui', training_api.splash)
    app.router.add_route('POST', '/plugin/training/flags', training_api.retrieve_flags)


async def _load_flags(data_svc):
    for filename in glob.iglob('plugins/training/data/certifications/**/*.yml', recursive=True):
        for cert in BaseWorld.strip_yml(filename):
            certification = Certification(identifier=cert['id'], name=cert['name'], access=BaseWorld.Access.APP)
            flag_number = 0
            for badge, data in cert['badges'].items():
                badge = Badge(name=badge)
                for number, module in enumerate(data['flags']):
                    flag_number += 1
                    loaded_module = import_module('plugins.training.app.%s' % module)
                    badge.flags.append(Flag(verify=getattr(loaded_module, 'verify'),
                                            number=flag_number,
                                            name=getattr(loaded_module, 'name'),
                                            challenge=getattr(loaded_module, 'challenge'),
                                            extra_info=getattr(loaded_module, 'extra_info')))
                certification.badges.append(badge)
            await data_svc.store(certification)
