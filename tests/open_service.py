"""IN PROGRESSS"""
import pytest
from s3Bucket.transfer_files import transfer_all_files_to_remote, transfer_specific_files_to_remote, \
    transfer_installation_scripts
from sshconnection.connect_remote import execute_commands


@pytest.mark.xfail(run=False)
def test_open_service():
    host = '10.0.0.138'
    user_name = 'Administrator'
    password = 'Automox2016'
    # installation_commands = [r'powershell cd bash_scripts ; powershell ./startservice.bat']
    installation_commands = ["powershell Start-Service -Name 'OpenSSH SSH Server'"]
    # logging.info(f"commands going to be exectued : {installation_commands}")
    ssh, stdin, stdout, stderr = execute_commands(host_name=host, user_name=user_name, password=password,
                                                  cmds=installation_commands)
    # logging.error(f"some error occured : {stderr}")
    pytest.xfail('Code is in progress')
