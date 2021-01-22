import glob
from importlib import import_module
import inspect
import os

from app.utility.base_world import BaseWorld
from plugins.training.app.c_badge import Badge
from plugins.training.app.c_certification import Certification
from plugins.training.app.c_exam import Exam
from plugins.training.app.c_fillinblank import FillInBlank
from plugins.training.app.c_flag import Flag
from plugins.training.app.c_multiplechoice import MultipleChoice
from plugins.training.app.c_navigator import Navigator
from plugins.training.app.training_api import TrainingApi

name = 'Training'
description = 'A certification course to become a CALDERA SME'
address = '/plugin/training/gui'

_question_types = dict(multiplechoice=MultipleChoice,
                       fillinblank=FillInBlank,
                       navigator=Navigator)


async def enable(services):
    data_svc = services.get('data_svc')
    await data_svc.apply('certifications')
    await _load_flags(data_svc)

    training_api = TrainingApi(services)
    app = services.get('app_svc').application
    app.router.add_static('/training', 'plugins/training/static/', append_version=True)
    app.router.add_route('GET', '/plugin/training/gui', training_api.splash)
    app.router.add_route('POST', '/plugin/training/flags', training_api.retrieve_flags)
    app.router.add_route('POST', '/plugin/training/reset_flag', training_api.reset_flag)


async def expansion(services):
    data_svc = services.get('data_svc')
    await _apply_hidden_access_to_loaded_files(data_svc)


async def _apply_hidden_access_to_loaded_files(data_svc):
    object_types = ['abilities', 'adversaries']
    for obj_typ in object_types:
        for filename in glob.iglob('plugins/training/data/'+obj_typ+'/**/*.yml', recursive=True):
            obj_id = os.path.splitext(os.path.basename(filename))[0]
            if obj_typ == 'abilities':
                match = dict(ability_id=obj_id)
            else:
                match = dict(adversary_id=obj_id)
            objects = await data_svc.locate(obj_typ, match=match)
            for obj in objects:
                obj.access = BaseWorld.Access.HIDDEN


async def _load_flags(data_svc):
    for filename in glob.iglob('plugins/training/data/certifications/**/*.yml', recursive=True):
        for cert in BaseWorld.strip_yml(filename):
            if cert.get('cert_type') and cert.get('cert_type') == 'exam':
                certification = Exam(identifier=cert['id'], name=cert['name'],
                                     description=cert.get('description', 'No description provided'),
                                     access=BaseWorld.Access.APP)
            else:
                certification = Certification(identifier=cert['id'], name=cert['name'],
                                              description=cert.get('description', 'No description provided'),
                                              access=BaseWorld.Access.APP)
            flag_number = 1
            for badge, data in cert['badges'].items():
                badge = Badge(name=badge)
                for number, module in enumerate(data['flags']):
                    module_name = 'plugins.training.app.%s' % module
                    try:
                        import_module(module_name)
                        filtered_registry = {k: v for k, v in Flag.registry.items() if v['module_name'] == module_name}
                        for cls, cls_attrs in filtered_registry.items():
                            badge.flags.append(_create_flag(cls, flag_number))
                            flag_number += 1
                    except ModuleNotFoundError:
                        module_name, cls_name = module_name.rsplit('.', 1)
                        cls = getattr(import_module(module_name), cls_name)
                        badge.flags.append(_create_flag(cls, flag_number))
                        flag_number += 1
                certification.badges.append(badge)
            await data_svc.store(certification)


def _create_flag(cls, flag_number):
    cls_params = inspect.signature(cls.__init__).parameters.keys()
    attrs = {attr: getattr(cls, attr, None) for attr, val in vars(cls).items() if getattr(cls, attr, None) is not None
             and attr in cls_params}
    return cls(**attrs, number=flag_number)
