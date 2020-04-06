from s3Bucket.transfer_files import transfer_agent_installation_scripts
from sshconnection.connect_remote import execute_commands


def agent_install(host_ip, user_name, password, realm, device_key):
    """
    This method is used to install the agent in the instance
    Args:
        host_ip: IP Address of the instance
        user_name: Username of the instance
        password: Password of the instance
        realm: To realm the instance needs to be added
        device_key: Device key of the Org

    Returns:
    """
    # Firstly Transfer all the required installation files to the host
    transfer_agent_installation_scripts(host_ip, user_name, password)

    # Finally Extract the installation files and execute commands
    setup_agent = "powershell cd Automation ; powershell ./extractzip.bat " + realm + ' ' + device_key
    commands = [setup_agent]
    execute_commands(host_name=host_ip, user_name=user_name, password=password, cmds=commands)


