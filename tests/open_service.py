"""IN PROGRESSS"""

from s3Bucket.transfer_files import transfer_all_files_to_remote, transfer_specific_files_to_remote, \
    transfer_installation_scripts
from sshconnection.connect_remote import execute_commands
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')
# Creating an object
# logger = logging.getLogger()
# # Setting the threshold of logger to DEBUG
# logger.setLevel(logging.DEBUG)

host = '10.0.0.138'
user_name = 'Administrator'
password = 'Automox2016'
logging.info("starting the commands")
# installation_commands = [r'powershell cd bash_scripts ; powershell ./startservice.bat']
installation_commands = ["powershell Start-Service -Name 'OpenSSH SSH Server'"]
logging.info(f"commands going to be exectued : {installation_commands}")
ssh, stdin, stdout, stderr = execute_commands(host_name=host, user_name=user_name, password=password,
                                              cmds=installation_commands)
logging.error(f"some error occured : {stderr}")