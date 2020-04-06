import boto3

session = boto3.Session(profile_name='dev')
ec2 = session.client('ec2')
client = session.resource('ec2')


def create_new_volume(snapshot_id, volume_name):
    """
    This method will create a new volume from the snapshot provided
    Args:
        snapshot_id: ID of the snapshot , to create a volume from
        volume_name: Name for the new volume created

    Returns:
        Returns new volume id created from the snapshot
    """
    # Create the volume from the snapshot
    volume = ec2.create_volume(
        AvailabilityZone='us-west-2a',
        Encrypted=False,
        Size=220,
        SnapshotId=snapshot_id,
        VolumeType='gp2',
        DryRun=False,
        TagSpecifications=[{
            'ResourceType': 'volume',
            'Tags': [{
                'Key': 'Name',
                'Value': volume_name
            }]
        }],
        MultiAttachEnabled=False
    )
    print(f"Create Volume Response : {volume}")
    print(f"Created Volume ID : {volume['VolumeId']}")
    new_volume_id = volume['VolumeId']
    return new_volume_id


def attach_volume(instance_id, new_volume_id):
    """
    This method will attach the volume provided to the specified instance
    Args:
        instance_id: ID of the instance
        new_volume_id: VolumeID of the volume provided

    Returns:

    """
    ec2.get_waiter('volume_available').wait(VolumeIds=[new_volume_id])
    print(f"Wait to attach volume")
    ec2.attach_volume(
        Device='/dev/sda1',
        InstanceId=instance_id,
        VolumeId=new_volume_id
    )
    print('New volume attaching')
    ec2.get_waiter('volume_in_use').wait(VolumeIds=[new_volume_id])
    print('New volume attached')


def detach_volume(volume_id):
    """
    This method will detach the volume from the instance based on the volumeID
    Args:
        volume_id: VolumeID of the volume to be detached

    Returns:

    """
    response = ec2.detach_volume(
        VolumeId=volume_id,
    )
    print("Volume is getting detached")
    ec2.get_waiter('volume_available').wait(VolumeIds=[volume_id])
    print("volume detached")
    print(f"Detach Volume Response : {response}")


def get_volume_state(instance_id):
    volumes = ec2.describe_instance_attribute(InstanceId=instance_id,
                                              Attribute='blockDeviceMapping')
    print(f"Volume Information : {volumes['BlockDeviceMappings']}")
    volume_state = volumes['BlockDeviceMappings'][0]['Ebs']['Status']
    print(f"Volume State: {volume_state}")
    return volume_state


def delete_volume(volume_id):
    """
    This method will delete the volume
    Args:
        volume_id: VolumeID of the volume to be deleted

    Returns:

    """
    ec2.delete_volume(
        VolumeId=volume_id,
        DryRun=False
    )



