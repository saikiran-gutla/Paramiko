import boto3
import botocore
from botocore.exceptions import ClientError, NoCredentialsError
import os

session = boto3.Session(profile_name='dev')


def upload_file_to_bucket(file_name, bucket_name, s3_file_name_in_bucket=None):
    """
    This Method Uploads file to S3 Bucket
    Args:
        file_name: Name of the file to upload
        bucket_name: Name of the S3 Bucket to upload
        s3_file_name_in_bucket: Name should be keep for the file in s3Bucket.
    Returns:
    """
    s3 = session.client('s3')
    if s3_file_name_in_bucket is None:
        s3_file_name_in_bucket = file_name
    try:
        print(f"File Name : {file_name} \n"
              f"File Name in S3 Bucket: {s3_file_name_in_bucket}\n"
              f"File Size : {os.path.getsize(file_name)} bytes\n"
              f"Uploading to Bucket: {bucket_name}")
        s3.upload_file(file_name, bucket_name, 'third_party' + '/' + 'Win' + '/' + s3_file_name_in_bucket)
        print(f"\n Finished Uploading the file : {file_name}")
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except ClientError:
        print("Error Logging into aws")
        return False


def download_file_from_bucket(s3_bucket_name, file_names, path=None):
    """

    Args:
        s3_bucket_name: Name of the S3 Bucket
        file_names: List of file names to download
        path: Path(sub folders) in the bucket

    Returns:

    """
    failed_files_to_download = []
    file_name = ''
    if path is None:
        path = ''
    try:
        s3 = session.resource('s3')
        print("Downloading files from bucket....\n")
        for file_name in file_names:
            try:
                s3.meta.client.download_file(s3_bucket_name, Key=path + file_name, Filename=file_name)
                print(f"File Downloaded : {file_name}")
            except FileNotFoundError:
                print(f"{file_name} is not available in S3 Bucket.")
                failed_files_to_download.append(file_name)
                raise FileNotFoundError

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"Failed Downloading File : {file_name}")
        else:
            raise
