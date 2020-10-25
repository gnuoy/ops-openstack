import ops_openstack.core
# ch_context needed for bluestore validation
import charmhelpers.contrib.openstack.context as ch_context
from ops.model import (
    ActiveStatus,
    BlockedStatus,
)


class BaseCephClientCharm(ops_openstack.core.OSBaseCharm):

    def check_bluestore_compression(self):
        try:
            self.get_bluestore_compression()
            return ActiveStatus()
        except ValueError as e:
            return BlockedStatus(
                'Invalid configuration: {}'.format(str(e)))

    def update_status(self, custom_checks=None):
        custom_checks = custom_checks or []
        super().update_status(
            custom_checks=custom_checks + [self.check_bluestore_compression])

    @staticmethod
    def get_bluestore_compression():
        """Get BlueStore Compression charm configuration if present.

        :returns: Dictionary of options suitable for passing on as keyword
                  arguments or None.
        :rtype: Optional[Dict[str,any]]
        :raises: ValueError
        """
        try:
            bluestore_compression = (
                ch_context.CephBlueStoreCompressionContext())
            bluestore_compression.validate()
        except KeyError:
            # The charm does not have BlueStore Compression options defined
            bluestore_compression = None
        if bluestore_compression:
            return bluestore_compression.get_kwargs()
