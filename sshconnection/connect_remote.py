import paramiko
import time


def ssh_connect(host_name, user_name, password):
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Connecting to host : ' + host_name)
        ssh.connect(hostname=host_name, username=user_name, password=password)
        print('Connected to host  : ' + host_name)
    except paramiko.AuthenticationException:
        print("Invalid Login Credentials")
        raise
    return ssh


def shh_connect_linux(host_name, user_name, key_file_name):
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Connecting to host : ' + host_name)
        ssh.connect(hostname=host_name, username=user_name, key_filename=key_file_name)
        print('Connected to host  : ' + host_name)
    except paramiko.AuthenticationException:
        print("Invalid Login Credentials")
        raise
    return ssh


def execute_command(host_name, user_name, password, cmd):
    ssh = ssh_connect(host_name=host_name, user_name=user_name, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    st = stdout.readlines()
    print(f"\nSTDIN : {stdin}\n"
          f"STDOUT : {stdout.readlines()}\n"
          f"STD ERROR :{stderr.readlines()}")
    for i in st:
        print(i)
    return stdin, stdout, stderr, ssh


def execute_commands(host_name, user_name, password, cmds):
    """
    This Method executes the commands passed in the list
    Args:
        host_name(str): IP address of the device
        user_name(str): UserName of the device
        password(str): Password of the device
        cmds(list): Commands to be executed in the device

    Returns:
        Returns STDIN,STDOUT,STDERROR after exxecuting the commands

    """
    ssh = ssh_connect(host_name=host_name, user_name=user_name, password=password)
    for command in cmds:
        print(f"Executing Command :{command}")
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(command)
        st = stdout.readlines()
        print(f"STDIN : {stdin}\n"
              f"STDOUT : {stdout.readlines()}\n"
              f"STD ERROR :{stderr.readlines()}")
        for i in st:
            print(i)
    return ssh


[{'osname': 'win10', 'ip_address': '10.2.26.42', 'username': 'testlab', 'password': 'Automox2016'},
 {'osname': 'win12', 'ip_address': '10.2.29.250', 'username': 'Administrator', 'password': 'Automox2016'}]
