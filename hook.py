import glob
from importlib import import_module
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
            flag_number = 0
            for badge, data in cert['badges'].items():
                badge = Badge(name=badge)
                for number, module in enumerate(data['flags']):
                    flag_number += 1
                    loaded_module = import_module('plugins.training.app.%s' % module)
                    if hasattr(loaded_module, 'flag_type'):
                        flag_type = getattr(loaded_module, 'flag_type')
                        attrs = {attr: getattr(loaded_module, attr) for attr in dir(loaded_module)
                                 if not attr.startswith('_') and attr != 'flag_type'}
                        badge.flags.append(_question_types[flag_type](**attrs, number=flag_number))
                    else:
                        additional_field_names = ['operation_name', 'adversary_id', 'agent_group']
                        additional_fields = dict()
                        for field in additional_field_names:
                            if hasattr(loaded_module, field):
                                additional_fields[field] = getattr(loaded_module, field)
                        badge.flags.append(Flag(verify=getattr(loaded_module, 'verify'),
                                                number=flag_number,
                                                name=getattr(loaded_module, 'name'),
                                                challenge=getattr(loaded_module, 'challenge'),
                                                extra_info=getattr(loaded_module, 'extra_info'),
                                                additional_fields=additional_fields))
                certification.badges.append(badge)
            await data_svc.store(certification)
