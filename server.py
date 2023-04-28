import socket
import os

# define the host and port
host = 'localhost'
port = 8000

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host, and a port
server_socket.bind((host, port))

# set the server to listen for incoming connections
server_socket.listen(1)

# define a dictionary of authorized users
authorized_users = {'sriya': '1235', 'samhitha': '2003'}

# define a dictionary of file contents
file_contents = {'/home/sriya/text.txt': 'This is the contents of the text file.',
                 '/home/samhitha/text.txt': 'This is the contents of the text file.'}

# loop to listen for incoming connections
while True:
    # wait for a client to connect
    client_socket, address = server_socket.accept()

    # receive the login credentials from the client
    message = client_socket.recv(1024).decode()
    username, password = message.split(":")

    # check if the user is authorized
    if username in authorized_users and authorized_users[username] == password:
        # send a response indicating that the user is authorized
        client_socket.send("authorized".encode())

        # loop to handle file read/write requests
        while True:
            # receive a file read/write request from the client
            request = client_socket.recv(1024).decode()
            command, path, contents = request.split(":") if ":" in request else (request, None, None)

            # handle the request based on the command
            if command == "load":
                # check if the file exists
                if os.path.exists(path) and os.path.isfile(path):
                    # read the file contents and send them to the client
                    with open(path, 'r') as f:
                        file_contents = f.read()
                    client_socket.send(file_contents.encode())
                else:
                    # send an error message to the client
                    client_socket.send("File not found".encode())

            elif command == "save":
                # check if the file exists
                if path in file_contents:
                    # update the file contents
                    file_contents[path] = contents

                    # send a response indicating that the file was saved successfully
                    client_socket.send("saved".encode())
                else:
                    # send an error message to the client
                    client_socket.send("File not found".encode())

            else:
                # send an error message to the client
                client_socket.send("Invalid command".encode())
    else:
        # send a response indicating that the user is not authorized
        client_socket.send("unauthorized".encode())

    # close the connection
    client_socket.close()
