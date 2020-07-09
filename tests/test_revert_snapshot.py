from AwsInstances.aws_volume_functions import get_volume_state, \
    detach_volume, create_new_volume, attach_volume, delete_volume
from AwsInstances.aws_instance_functions import get_instance_status, stop_instance, get_volume_id_of_instance, \
    start_instance

instance_id = "i-0fb7fda74c7fd8e52"
volume_name = 'axtest-policy-config-win-2012-base'
snapshot_id = 'snap-03d2d2bb9c7667501'


def test_revert_third_party_instances():
    # check the instance status
    status = get_instance_status(instance_id)
    if status:
        # Stop the instance
        stop_instance(instance_id=instance_id)

    print('Instance is not running')
    # Get Volume state
    volume_state = get_volume_state(instance_id=instance_id)

    # check volume is attached or not(if attached detach the volume)
    if volume_state == 'attached':
        volume_id = get_volume_id_of_instance(instance_id=instance_id)
        # Detach volume
        detach_volume(volume_id=volume_id)
        
        # Deleting the old Volume
        delete_volume(volume_id)
        print('Old volume removed')

    # Create the volume from the snapshot
    created_volume_id = create_new_volume(snapshot_id, volume_name)

    # Attach the created volume
    attach_volume(instance_id=instance_id, new_volume_id=created_volume_id)

    # Start the instance
    start_instance(instance_id=instance_id)
