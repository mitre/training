import glob
from importlib import import_module

from app.utility.base_world import BaseWorld
from plugins.training.app.c_flag import Flag
from plugins.training.app.training_api import TrainingApi

name = 'Training'
description = 'A certification course to become a CALDERA SME'
address = '/plugin/training/gui'


async def enable(services):
    data_svc = services.get('data_svc')
    await data_svc.apply('flags')
    await _load_flags(data_svc)

    training_api = TrainingApi(services)
    app = services.get('app_svc').application
    app.router.add_static('/training', 'plugins/training/static/', append_version=True)
    app.router.add_route('GET', '/plugin/training/gui', training_api.splash)
    app.router.add_route('POST', '/plugin/training/flags', training_api.retrieve_flags)


async def _load_flags(data_svc):
    for flag in glob.iglob('plugins/training/app/flags/**/**.py', recursive=True):
        module = flag.replace('/', '.').replace('.py', '')
        loaded_module = import_module(module)
        await data_svc.store(Flag(verify=getattr(loaded_module, 'verify'),
                                  number=1,
                                  name=getattr(loaded_module, 'name'),
                                  description=getattr(loaded_module, 'description')))
