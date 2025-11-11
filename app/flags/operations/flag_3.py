import logging
from plugins.training.app.c_flag import Flag

class OperationsFlag3(Flag):
    name = 'Empty Op'

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
            logging.error("[training.flag3] data_svc is None!")
            return False

        operations = await data_svc.locate('operations')
        for op in operations:
            logging.info(f"[training.flag3] Checking operation '{op.name}' | state={op.state}, group={op.group}, adversary_id={getattr(op.adversary, 'adversary_id', None)}")

            # Gather all link lists that might exist
            chain_links = getattr(op, 'chain', []) or []
            potential_links = getattr(op, 'potential_links', []) or []
            manual_links = getattr(op, 'links', []) or []

            total_links = len(chain_links) + len(potential_links) + len(manual_links)

            logging.info(f"[training.flag3] Found {len(chain_links)} chain links, {len(potential_links)} potential links, {len(manual_links)} manual links (total={total_links})")

            # Verify completion conditions
            if (
                op.finish
                and getattr(op.adversary, 'adversary_id', None) == 'ad-hoc'
                and total_links >= 5
                and not op.group
            ):
                logging.info(f"[training.flag3] ✅ Operation '{op.name}' meets all criteria!")
                return True

        logging.info("[training.flag3] ❌ No operation met the criteria.")
        return False