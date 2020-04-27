import boto3


class CreateInstance:
    def __init__(self):
        machine_os_types = []
        available_end_to_end_machine_images = {"win8": "ami-0de1500c5ca1ebacd", "win10": "ami-0cd131414ef080a6c",
                                               "win12": "ami-08894ac0083738237", "win16": "ami-0dd092c5f3d473288",
                                               "ubuntu": "ami-07033edde322aa950", "centos": "ami-0c85a3f6f06232c16",
                                               "fedora": "ami-0ecd030c6677c164c", "redhat": "ami-0eb06b646ddf47b94",
                                               "win10-thirdparty-32bitsw": "ami-0e6441f96b704c5bf",
                                               "win8-thirdparty": "ami-045031c25d8840f0d",
                                               "Win10-Thirdpartysw": "ami-0b4e20a007e91f10e",
                                               "Win12-thirdparty": "ami-058a8402ffa640a23"}
        vpc_type = {"stg": "vpc-37f7184e", "qe": "vpc-0447ab8cb096cc1f5"}
        subnet_type = {"stg": "subnet-05c7d6b54f3abf084", "qe": "subnet-0c28ef8cbffb780e6"}
        security_groups = {"stg": "sg-14de6468", "qe": "sg-0b789376e933c4fc8"}
        vpc_subnet_type = input(f"VPC/ SUBNET type:\n"
                                f"1.STAGING\n"
                                f"2.QE\n"
                                f"Choose your option : ")

        if vpc_subnet_type == str(1):
            self.vpc_type_id = vpc_type['stg']
            self.subnet_type_id = subnet_type['stg']
            self.security_group_id = security_groups['stg']
        elif vpc_subnet_type == str(2):
            self.vpc_type_id = vpc_type['qe']
            self.subnet_type_id = subnet_type['qe']
            self.security_group_id = security_groups['qe']
        else:
            print("Wrong Option")
        # CODE TO SELECT THE TYPE OF INSTANCE TO CREATE
        for machine_name in available_end_to_end_machine_images.keys():
            machine_os_types.append(machine_name)
        print(f"AVAILABLE AMI'S TO CREATE INSTANCE")
        for i in range(len(machine_os_types)):
            print(f"{i + 1} : {machine_os_types[i]}")
        end_point_option = int(input("Choose Your Option : "))
        for i in range(len(machine_os_types) + 1):
            if str(i) == str(end_point_option):
                self.machine_os = machine_os_types[i - 1]
                self.end_point_ami_id = available_end_to_end_machine_images[self.machine_os]
                break
        self.create_instance()

    def create_instance(self):
        name_of_instance = 'qa-ax-manual-' + self.machine_os + '-script'
        session = boto3.Session(profile_name='dev')
        ec2 = session.resource('ec2')
        vpc = ec2.Vpc(self.vpc_type_id)
        response = ec2.create_instances(
            ImageId=self.end_point_ami_id,
            InstanceType='t2.xlarge',
            MaxCount=1,
            MinCount=1,
            Monitoring={
                'Enabled': False
            },
            SubnetId=self.subnet_type_id,
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 220,
                        'VolumeType': 'gp2'
                    },
                },
            ],
            SecurityGroupIds=[
                self.security_group_id,
            ]
        )
        for instance in ec2.instances.all():
            if instance.id == response[0].id:
                print(f"INSTANCE ID: {response[0].id}\n"
                      f"IP ADDRESS : {instance.private_ip_address}")
                break


create_instance_obj = CreateInstance()
