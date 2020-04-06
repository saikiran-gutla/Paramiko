"""This file contains the methods to transfer files to the remote machine"""
import boto3
from sshconnection.remote_transfer import upload_files_to_remote_device, \
    upload_files_to_remote_device_specific_path

session = boto3.Session(profile_name='dev')


def transfer_specific_files_to_remote(hostname, username, password, bucket_name, upload_files_list, folder_name=None,
                                      path=None):
    """
        This method transfers the specified files in the list to the remote machine.
        If the files are in the Bucket directly instead of sub folders, don't pass the path.
    Args:
        folder_name: Folder name to be created and transfer files to created folder.
        hostname: Ip address of the device
        username: Username of the device
        password: Password of the device
        bucket_name: S3 Bucket name
        upload_files_list: List of the file names to transfer the files
        path: Path of the files in the s3 bucket

    Returns:

    """
    upload_files_to_remote_device(host_name=hostname, user_name=username, password=password,
                                  bucket_name=bucket_name, path=path, folder_name=folder_name,
                                  upload_files=upload_files_list)


def transfer_all_files_to_remote(hostname, username, password, bucket_name, folder_name=None, path=None):
    """
    This method transfers all files present in the bucket to remote machine specified.
    If the files are in the Bucket directly instead of sub folders, don't pass the path.
    Args:
        folder_name: Name of the folder to create in remote machine and upload files into it.
        hostname: IP address of the remote machine.
        username: UserName of the remote machine.
        password: Password of the remote machine.
        bucket_name: Name of the bucket to download files from.
        path: Path of the files available in the bucket.
        Note:
            1.Need to specify the path of the files if they are in the sub folders of the bucket and place '/'
            at the end of the path.
    Returns:
        Returns all the file names in the specified path of the bucket in the form of a list.
    """
    all_file_names = []
    if path is None:
        s3 = session.client('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            key = obj.key
            all_file_names.append(key)
        upload_files_to_remote_device(host_name=hostname, user_name=username, password=password,
                                      bucket_name=bucket_name, folder_name=folder_name,
                                      upload_files=all_file_names)

    else:
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=path))
        for i in range(0, len(objs)):
            if objs[i].key.split(path)[1] != '':
                if '/' not in objs[i].key.split(path)[1]:
                    all_file_names.append(objs[i].key.split(path)[1])
        upload_files_to_remote_device(host_name=hostname, user_name=username, password=password,
                                      bucket_name=bucket_name, path=path, folder_name=folder_name,
                                      upload_files=all_file_names)
    return all_file_names


def transfer_all_files_to_remote_path(hostname, username, password, bucket_name, folder_path, local_files_path,
                                      folder_name=None,
                                      path=None):
    """
            This method is still under progress need to shorten this method.


    This method transfers all files from the bucket to remote machine specified.
    If the files are in the Bucket directly instead of sub folders, don't pass the path.
    Args:
        local_files_path:
        folder_path: Folder path in remote machine to upload files.
        folder_name: Name of the folder to create in remote machine and upload files into it.
        hostname: IP address of the remote machine.
        username: UserName of the remote machine.
        password: Password of the remote machine.
        bucket_name: Name of the bucket to download files from.
        path: Path of the files available in the bucket.
        Note:
            1.Need to specify the path of the files if they are in the sub folders of the bucket and place '/'
            at the end of the path.
    Returns:

    """
    print(folder_path)
    all_file_names = []
    if path is None:
        s3 = boto3.client('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            key = obj.key
            all_file_names.append(key)
        upload_files_to_remote_device_specific_path(host_name=hostname, user_name=username, password=password,
                                                    bucket_name=bucket_name, upload_files=all_file_names,
                                                    folder_path=folder_path, local_files_path=local_files_path,
                                                    folder_name=folder_name)

    else:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=path))
        for i in range(0, len(objs)):
            if objs[i].key.split(path)[1] != '':
                if '/' not in objs[i].key.split(path)[1]:
                    all_file_names.append(objs[i].key.split(path)[1])
        upload_files_to_remote_device_specific_path(host_name=hostname, user_name=username, password=password,
                                                    bucket_name=bucket_name, path=path, upload_files=all_file_names,
                                                    folder_path=folder_path, folder_name=folder_name,
                                                    local_files_path=local_files_path)
    return True


def transfer_installation_scripts(hostname, username, password):
    """
    This Method Transfers the installation batch files(msi,exe) to the remote host
    Args:
        hostname: Ip address of the device
        username: Username of the device
        password: Password of the device
    Returns:

    """
    bucket_name = 'automox-qe-input-artifacts'
    path = 'setup_instance/bash_files/'
    folder_name = 'bash_scripts'
    transfer_all_files_to_remote(hostname=hostname, username=username, password=password,
                                 bucket_name=bucket_name, path=path, folder_name=folder_name)


def transfer_agent_installation_scripts(hostname, username, password):
    """
    This Method Transfers agent installation files to the remote host
    :param hostname:
    :param username:
    :param password:
    :return:
    """
    bucket_name = 'automox-qe-input-artifacts'
    path = 'setup_instance/Agent_install/'
    folder_name = 'Automation'
    upload_files_list = ['7za.exe', 'extractzip.bat', 'InstallAgent.zip']
    transfer_specific_files_to_remote(hostname=hostname, username=username, password=password,
                                      bucket_name=bucket_name, path=path, folder_name=folder_name,
                                      upload_files_list=upload_files_list)
