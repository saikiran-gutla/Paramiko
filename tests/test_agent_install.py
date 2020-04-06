from installation.install_agent import agent_install
import pytest

host_ip = '10.0.0.211'
user_name = 'testlab'
password = 'Automox2016'
realm = 'stg'
device_key = 'df8efb25-d0de-463f-9e69-57d6b35ab70a'

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

    agent_install(host_ip , user_name, password, realm, device_key)
# E           paramiko.ssh_exception.AuthenticationException: Authentication failed.
