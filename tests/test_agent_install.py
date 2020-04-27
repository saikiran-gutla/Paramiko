from AwsInstances.aws_create_instance import create_aws_instance
from installation.install_agent import agent_install
import pytest

host_ip = '10.0.0.153'
user_name = 'testlab'
password = 'Automox2016'
realm = 'stg'
device_key = '412e3371-59c5-4c16-afff-814583ac78bf'


@pytest.mark.xfail(run=False)
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
    pytest.xfail('This Script is not required to run. Skipping this test')
# E           paramiko.ssh_exception.AuthenticationException: Authentication failed.
