import boto3

session = boto3.Session(profile_name='dev')
ec2 = session.client('ec2')
client = session.resource('ec2')


def start_instance(instance_id):
    """
    This method will start the instance based on the given InstanceID
    Args:
        instance_id: InstanceID of the instance

    Returns:

    """
    print('Starting the instance')
    ec2.start_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter('instance_running')
    print('Instance is running now')
    return waiter


def stop_instance(instance_id):
    """
    This Method will Stop the Instance based on the given InstanceID
    Args:
        instance_id: InstanceID of the instance

    Returns:

    """
    print("stopping the instance")
    ec2.stop_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter('instance_stopped')
    print("still waiting to get instance stopped")
    waiter.wait(InstanceIds=[instance_id])
    return waiter


def get_volume_id_of_instance(instance_id):
    """
    This method will return the VolumeID of the instance
    Args:
        instance_id: InstanceID of the instance

    Returns:

    """
    volumes = ec2.describe_instance_attribute(InstanceId=instance_id,
                                              Attribute='blockDeviceMapping')
    print(f"Volume Information : {volumes['BlockDeviceMappings']}")
    volume_id = volumes['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    print(f"Volume ID of instance: {volume_id}")
    return volume_id


def get_instance_status(instance_id):
    instance = client.Instance(instance_id)
    if instance.state['Name'] == 'running':
        status = True
    else:
        status = False
    return status
