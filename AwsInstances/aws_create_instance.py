"""This code is used to create the instances"""
import boto3

from AwsInstances.aws_instance_functions import wait_until_instance_running
from AwsLoggers.aws_loggers import get_logger


def create_aws_instance(machines_to_create, realm):
    """
    This method will create instances based on the AMI names list provided
    Args:
        machines_to_create(list): List of machine names to create
        realm: Realm name to create machines for

    Returns:
            Returns a list contains OsName,IpAddress,Username,Password.
    """
    global USERNAME, PASSWORD
    session = boto3.Session(profile_name='dev')
    ec2 = session.resource('ec2')
    __my_logger = get_logger("Create Aws Instance")
    available_end_to_end_machine_images = {"win8": "ami-0de1500c5ca1ebacd",
                                           "win10": "ami-0cd131414ef080a6c",
                                           "win12": "ami-08894ac0083738237",
                                           "win16": "ami-0dd092c5f3d473288"}
    subnet_type = {"stg": "subnet-05c7d6b54f3abf084", "qe": "subnet-0c28ef8cbffb780e6"}
    security_groups = {"stg": "sg-14de6468", "qe": "sg-0b789376e933c4fc8"}
    not_available_machines = []
    available_machines_to_create = []
    instance_overall_details = []
    wait_for_running = []
    if realm not in ['stg', 'qe']:
        __my_logger.error('realm not available')

    for machine in machines_to_create:
        if machine not in available_end_to_end_machine_images.keys():
            # raise Instance_Not_Available('Instance Type provided is not available to create')
            not_available_machines.append(machine)
        else:
            available_machines_to_create.append(machine)
    if len(not_available_machines) > 0:
        __my_logger.debug('Failed in Creating Machiness: %s ', not_available_machines)
    for os_name in available_machines_to_create:
        # create a new EC2 instance
        response = ec2.create_instances(
            ImageId=available_end_to_end_machine_images[os_name],
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.xlarge',
            KeyName='automation-dev',
            SubnetId=subnet_type[realm],
            SecurityGroupIds=[security_groups[realm]],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 220,
                        'VolumeType': 'gp2'
                    },
                },
            ]
        )
        if os_name in ['win8', 'win10']:
            USERNAME = 'testlab'
            PASSWORD = 'Automox2016'
        elif os_name in ['win12', 'win16']:
            USERNAME = 'Administrator'
            PASSWORD = 'Automox2016'
        # Name the instance created
        name_of_instance = 'qa-ax-manual-' + realm + '-' + os_name + '-script'
        wait_until_instance_details = []
        for instance in ec2.instances.all():
            if instance.id == response[0].id:
                __my_logger.info("INSTANCE ID: %s \tIP ADDRESS : %s \t INSTANCE NAME : %s",
                                 response[0].id, instance.private_ip_address, name_of_instance)
                wait_for_running.append(instance.id)
                if os_name in ['win8', 'win10']:
                    USERNAME = 'testlab'
                    PASSWORD = 'Automox2016'
                elif os_name in ['win12', 'win16']:
                    USERNAME = 'Administrator'
                    PASSWORD = 'Automox2016'
                instance_overall_details.append(
                    {'osname': os_name,
                     'ip_address': instance.private_ip_address,
                     'username': USERNAME,
                     'password': PASSWORD})
                wait_until_instance_details.append(instance.id)
                ec2.create_tags(
                    Resources=[
                        response[0].id,
                    ],
                    Tags=[
                        {
                            'Key': 'Name',
                            'Value': name_of_instance
                        },
                    ]
                )
                break

    for instance in wait_for_running:
        wait_until_instance_running(instance)
    __my_logger.info('overall : %s', instance_overall_details)
    return instance_overall_details
