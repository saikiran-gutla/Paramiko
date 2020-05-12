from AwsInstances.aws_create_instance import create_aws_instance
from installation.install_agent import agent_install
import pytest

from sshconnection.connect_remote import execute_commands

host_ip = '10.2.23.140'
user_name = 'testlab'
password = 'Automox2016'
realm = 'stg'
device_key = '1b5f1713-5c66-4a07-998c-99748c6df105'


@pytest.mark.install_agent
def test_install_agent():
    """
    This test case will install agent in specified device.
    Args:
        host_ip: IP Address of the instance
        username: Username of the instance
        userpass: Password of the instance
        realm: To realm the instance needs to be added
        access_key: Device key of the Org

    Returns:

    """
    agent_install(host_ip, user_name, password, realm, device_key)

