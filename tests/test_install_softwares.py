from installation.install_files import install_software_files
from s3Bucket.transfer_files import transfer_specific_files_to_remote, transfer_all_files_to_remote, \
    transfer_installation_scripts
import pytest

host = '10.0.0.138'
user_name = 'Administrator'
password = 'Automox2016'
bucket_name = 'automox-iso'
path = 'third_party/Win/7-Zip/'
all_file_names = ['7z1604.exe']


@pytest.mark.install_specific_files
def test_install_specific_files():
    # Transfer Specific files if required to the remote machine

    transfer_specific_files_to_remote(hostname=host, username=user_name, password=password, bucket_name=bucket_name,
                                      upload_files_list=all_file_names, path=path)
    # Transfer the installation scripts to the endpoint
    transfer_installation_scripts(host, user_name, password)

    install_software_files(all_file_names=all_file_names, host=host, user_name=user_name, password=password)


@pytest.mark.install_all_files
def test_install_all_files():
    # Transfer all files to the remote machine
    all_software = transfer_all_files_to_remote(hostname=host, username=user_name, password=password,
                                                bucket_name=bucket_name, path=path)
    # Transfer the installation scripts to the endpoint
    transfer_installation_scripts(host, user_name, password)

    # Install the transferred software using the transferred installation bash scripts
    install_software_files(all_file_names=all_software, host=host, user_name=user_name, password=password)
