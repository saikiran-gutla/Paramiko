from sshconnection.connect_remote import execute_commands


def install_software_files(all_file_names, host, user_name, password):
    installation_commands = []
    unsupported_files = []
    print("\nInstalling Files.........")
    for installer_file in all_file_names:
        if installer_file[-3:] == "exe":
            cmd = r'powershell cd bash_scripts ; powershell ./installexe.bat C:\Users\\' + user_name + '\\UploadedFiles\\' + installer_file
            installation_commands.append(cmd)
        elif installer_file[-3:] == "msi":
            cmd = r'powershell cd bash_scripts ; powershell ./installmsi.bat C:\Users\\' + user_name + '\\UploadedFiles\\' + installer_file
            installation_commands.append(cmd)
        else:
            unsupported_files.append(installer_file)
            print(f"{installer_file} is not supported")

    print(f"Commands Going to be installed:\n"
          f"{installation_commands}")

    execute_commands(host_name=host, user_name=user_name, password=password, cmds=installation_commands)
