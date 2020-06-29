from app.utility.base_world import BaseWorld


name = 'Acquire Cron Jobs Baseline'
challenge = 'Run the appropriate setup ability in the \'Blue Manual\' operation to acquire a list of currently ' \
            'existing cron jobs on the *nix machine.'
extra_info = """"""


async def verify(services):
    for op in await services.get('data_svc').locate('operations',
                                                    match=dict(access=BaseWorld.Access.BLUE, name='Blue Manual')):
        if cron_jobs_baseline_found(op):
            return True
    return False


def cron_jobs_baseline_found(op):
    return '' in [link.ability.ability_id for link in op.chain if link.finish]
