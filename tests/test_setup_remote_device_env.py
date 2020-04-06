"""IN PROGRESS"""

import os
from s3Bucket.transfer_files import transfer_all_files_to_remote, transfer_all_files_to_remote_path
from sshconnection.remote_transfer import upload_files_to_remote_device_specific_path


def test_setup_axbin():
    """
    This method copies the axbin, .ssh files to remote instance
    Returns:
    STEPS:
    1. Adds the Axbin files to the remote machine
    2. Adds the .ssh files in the remote machine
    3. Sends the Power shell Installer file to the machine
    4. Creates 'tmp' folder in the machine
    """
    # 1. Upload the axbin files
    host_name = '10.0.0.198'
    user_name = 'testlab'
    password = 'Automox2016'
    bucket_name = 'automox-qe-input-artifacts'
    folder_name = 'axbin'
    path = 'setup_instance/axbin/'
    folder_path = 'C:\\'
    local_files_path = os.getcwd()
    flag = transfer_all_files_to_remote_path(hostname=host_name, username=user_name, password=password,
                                             bucket_name=bucket_name,
                                             folder_name=folder_name, path=path, folder_path=folder_path,
                                             local_files_path=local_files_path)
    if not flag:
        print(f"Error occured uploading files")
        raise
    print("Axbin setup success")
