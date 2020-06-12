from app.utility.base_world import BaseWorld


class BaseFlag:
    """
    A collection of static functions to be used by training flags.
    """

    @staticmethod
    async def does_agent_exist(services, group):
        return len(await services.get('data_svc').locate('agents', match=dict(group=group)))

    @staticmethod
    async def is_operation_started(services, op_name):
        return len(await services.get('data_svc').locate('operations', match=dict(name=op_name)))

    @staticmethod
    async def start_operation(services, op_name, group, adv_id):
        access = dict(access=[BaseWorld.Access.HIDDEN])
        data = dict(name=op_name, group=group, adversary_id=adv_id,
                    planner='batch', atomic_enabled=1, hidden=True)
        await services.get('rest_svc').create_operation(access=access, data=data)

    @staticmethod
    async def is_operation_successful(services, op_name, traits=[], num_links=1):
        operation = (await services.get('data_svc').locate('operations', match=dict(name=op_name)))[0]
        if len(operation.chain) == num_links and \
                all(trait in [f.trait for f in operation.all_facts()] for trait in traits):
            return True
        return False

    @staticmethod
    async def cleanup_operation(services, op_name):
        await services.get('rest_svc').delete_operation(data=dict(name=op_name))
