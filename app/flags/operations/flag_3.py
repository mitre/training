import logging

from plugins.training.app.c_flag import Flag

log = logging.getLogger(__name__)


class OperationsFlag3(Flag):
    name = 'Empty operation'

    challenge = (
        'Run and finish an operation without selecting any agent groups or adversary profiles. Add at least 5 manual '
        'or potential links to the operation before finishing the operation.'
    )

    extra_info = (
        'During an autonomous adversary emulation exercise, the operation will only run tasks in the adversary profile. '
        'Manual and potential links allow an operator to "toss in" additional TTPs into a live, autonomous operation.'
    )

    async def verify(self, services):
        data_svc = services.get('data_svc')
        if not data_svc:
            log.debug("[training.flag3] data_svc is None!")
            return False

        operations = await data_svc.locate('operations')
        for op in operations:
            adversary = getattr(op, 'adversary', None)
            adversary_id = getattr(adversary, 'adversary_id', None)
            log.debug("[training.flag3] Checking operation '%s' | state=%s, group=%s, adversary_id=%s",
                      op.name, op.state, op.group, adversary_id)

            # Gather all link lists that might exist
            chain_links = getattr(op, 'chain', []) or []
            potential_links = getattr(op, 'potential_links', []) or []
            manual_links = getattr(op, 'links', []) or []

            total_links = len(chain_links) + len(potential_links) + len(manual_links)

            log.debug("[training.flag3] Found %d chain links, %d potential links, %d manual links (total=%d)",
                      len(chain_links), len(potential_links), len(manual_links), total_links)

            # Verify completion conditions
            if (
                op.finish
                and adversary_id == 'ad-hoc'
                and total_links >= 5
                and not op.group
            ):
                log.debug("[training.flag3] Operation '%s' meets all criteria!", op.name)
                return True

        log.debug("[training.flag3] No operation met the criteria.")
        return False
