from sshconnection.connect_remote import ssh_connect, execute_command, execute_commands
from s3Bucket.s3_files_operations import download_file_from_bucket
import os


def download_file_from_remote_device(host_name, user_name, password):
    """
    This method will download the specified file from the remote machine.
    Args:
        host_name:
        user_name:
        password:

    Returns:

    """
    ssh = ssh_connect(host_name, user_name, password)
    sftp_client = ssh.open_sftp()
    # SOURCE PATH ////// DESTINATION PATH
    sftp_client.get('C:/Users/hello.py', 'received.txt')
    print('file downloaded')


def upload_files_to_remote_device(host_name, user_name, password, bucket_name, upload_files, folder_name, path=None):
    """
        This Method will Upload files to the remote device.
        Can Provide the folder name to create and transfer files to them.
    Args:
        folder_name: Folder name in remote to upload
        path(str): Path(Sub folders) containing the files
        bucket_name(str): Name of the Bucket to Upload files from.
        password(str): Password of the Device
        user_name(str): username of the device
        host_name(str): Host IP address of the address.
        upload_files(list): List of file names to upload to remote machine

    Returns:

    """
    failed_uploading_files = []
    file_name = ''
    if folder_name is None:
        folder_name = 'UploadedFiles'
    print(f"\nCreating Folder : {folder_name}\n"
          f"S3 Bucket files path  : {path}")
    try:
        stdin, stdout, stderr, ssh = execute_command(host_name, user_name, password, cmd='mkdir ' + folder_name)
        download_file_from_bucket(s3_bucket_name=bucket_name, file_names=upload_files, path=path)
        print('\nUploading Files.........')
        for file_name in upload_files:
            try:
                sftp_client = ssh.open_sftp()
                sftp_client.put(str(os.getcwd()) + '/' + str(file_name),
                                'C:\\Users\\' + user_name + '\\' + folder_name + "\\" + file_name)
                print(f"File Uploaded : {file_name}")
            except FileNotFoundError:
                print(f"file not found : {file_name}")
                failed_uploading_files.append(file_name)
        if len(failed_uploading_files) > 0:
            print(f'Failed Files to Upload : {failed_uploading_files}\n'
                  f'Make Sure File name is correct as per s3 bucket and file available in S3')
        print(f"\nRemoving files from local machine")
    except FileNotFoundError:
        print(f'\nFailed Uploading File: {file_name}')
    finally:
        for file in upload_files:
            try:
                path = os.path.join(os.getcwd(), file)
                os.remove(path=path)
                print(f'{file} removed from Local system')
            except FileNotFoundError:
                print(f"File not found for removing {file}")


# The Below Method is not emergency now keeping it side
def upload_files_to_remote_device_specific_path(host_name, user_name, password, bucket_name, upload_files, folder_path,
                                                folder_name, local_files_path, path=None):
    """
        This method is still under progress need to shorten this method.
    Args:
        folder_name:
        local_files_path:
        folder_path:
        path(str): Path(Sub folders) containing the files
        bucket_name(str): Name of the Bucket to Upload files from.
        password(str): Password of the Device
        user_name(str): username of the device
        host_name(str): Host IP address of the address.
        upload_files(list): List of file names to upload to remote machine

    Returns:

    """
    folder = 'mkdir ' + folder_name
    li = ["powershell cd / ; powershell '+folder"]
    failed_uploading_files = []
    file_name = ''
    if folder_name is None:
        folder_name = 'UploadedFiles'
    if folder_path is None:
        folder_path = 'C:\\Users\\' + user_name + '\\' + folder_name

    print(f"Creating Folder : {folder_name}\n"
          f"S3 Bucket files path  : {path}\n"
          f"Folder Path  : {folder_path}\n"
          f"Local Files Path : {local_files_path}")
    try:
        ssh = execute_commands(host_name=host_name, user_name=user_name, password=password)
        download_file_from_bucket(s3_bucket_name=bucket_name, file_names=upload_files, path=path)
        print('\nUploading Files.........')
        for file_name in upload_files:
            try:
                sftp_client = ssh.open_sftp()
                sftp_client.put(local_files_path + '/' + str(file_name),
                                folder_path + "\\" + folder_name + "\\" + file_name)
                print(f"File Uploaded : {file_name}")
            except FileNotFoundError:
                print(f"file not found : {file_name}")
                failed_uploading_files.append(file_name)
    except FileNotFoundError:
        print(f'\nFailed Uploading File: {file_name}')
    if len(failed_uploading_files) > 0:
        print(f'Failed Files to Upload : {failed_uploading_files}\n'
              f'Make Sure File name is correct as per s3 bucket and file available in S3')
    print(f"\nRemoving files from local machine")
    for file in upload_files:
        try:
            path = os.path.join(local_files_path, file)
            os.remove(path=path)
            print(f'{file} removed from Local system')
        except FileNotFoundError:
            print(f"File not found for removing {file}")
