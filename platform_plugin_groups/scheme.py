from openedx.core.djangoapps.course_groups.api import get_group, get_group_info_for_group
from xmodule.partitions.partitions import NoSuchUserPartitionGroupError


class GroupPartitionScheme:
    """
    This scheme uses lms cohorts (CourseUserGroups) and group-partition
    mappings (CourseUserGroupPartitionGroup) to map lms users into Partition
    Groups.
    """

    @classmethod
    def get_grouped_user_partition(cls, course):
        for user_partition in course.user_partitions:
            if user_partition.scheme == cls:
                return user_partition

        return None

    @classmethod
    def get_group_for_user(cls, course_key, user, user_partition):
        """
        Returns the (Content) Group from the specified user partition to which the user
        is assigned, via their group-type membership and any mappings from groups
        to partitions / (content) groups that might exist.

        If the user has no group-type mapping, or there is no (valid) group ->
        partition group mapping found, the function returns None.
        """
        group = get_group(user, course_key)
        if group is None:
            return None

        group_id, partition_id = get_group_info_for_group(group)
        if partition_id is None:
            return None

        if partition_id != user_partition.id:
            return None

        try:
            return user_partition.get_group(group_id)
        except NoSuchUserPartitionGroupError:
            return None
