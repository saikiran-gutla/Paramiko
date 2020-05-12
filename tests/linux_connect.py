import paramiko

from sshconnection.connect_remote import shh_connect_linux, execute_commands, ssh_connect
import subprocess

host_ip = "10.2.9.225"
user_name = 'ec2-user'
password = "Automox2016"
curl_script = 'curl -sS "https://console.stg.automox-dev.com/downloadInstaller?accesskey=22e2e8c6-5cea-487b-8e26-b8bf2de1bc4d" | sudo bash'
cmd = [curl_script, 'sudo service amagent start', 'sudo service amagent stop', 'sudo chmod 777 /etc/default']
ssh = None
try:
    ssh = shh_connect_linux(host_ip, user_name,
                            key_file_name='/Users/coppertaurus/PycharmProjects/Aws/KeyFiles/sshkey.pub')
    execute_commands(ssh, cmd)
    subprocess.run(["scp", "/Users/coppertaurus/PycharmProjects/Aws/KeyFiles/amagent",
                    user_name + '@' + host_ip + ':' + '/etc/default'])
    # if user_name in ['ec2-user']:
    #     start = ['sudo amagent --apiurl https://api.stg.automox-dev.com', 'sudo service amagent restart']
    # elif user_name in ['ubuntu', 'fedora']:
    start = ['sudo /opt/amagent/amagent --apiurl https://api.stg.automox-dev.com', 'sudo service amagent restart']
    execute_commands(ssh, start)
except paramiko.AuthenticationException:
    print("Invalid Login Credentials")
    raise
