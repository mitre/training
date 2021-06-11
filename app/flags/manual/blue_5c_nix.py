from plugins.training.app.base_flag import BaseFlag
from plugins.training.app.c_flag import Flag
from app.utility.base_world import BaseWorld


class ManualBlue5cNix(Flag):
    name = 'Find Changes to Bash Profile'
    challenge = 'Within a minute of this flag activating, the .bashrc file of the user used to deploy the red ' \
                'agent on the *nix machine will have been modified. Run the appropriate detection ability in the ' \
                '\'Blue Manual\' operation to find the modified profile.'
    extra_info = """"""
    additional_fields = dict(operation_name='training_manual_5a',
                             adversary_id='08619190-9eb5-4f35-97e1-0dafe04e0203',
                             agent_group='cert-nix')

    async def verify(self, services):
        async def is_flag_satisfied():
            for op in await services.get('data_svc').locate('operations', match=dict(access=BaseWorld.Access.BLUE,
                                                                                     name='Blue Manual')):
                if is_modified_profile_found(op):
                    return True
            return False

        def is_modified_profile_found(op):
            return op.ran_ability_id('930236c2-5397-4868-8c7b-72e294a5a376') and \
                   'has_been_modified' in set(f.trait for f in await op.all_facts())

        return await BaseFlag.standard_verify_with_operation(services, self.additional_fields['operation_name'],
                                                             self.additional_fields['adversary_id'],
                                                             self.additional_fields['agent_group'],
                                                             is_flag_satisfied)
