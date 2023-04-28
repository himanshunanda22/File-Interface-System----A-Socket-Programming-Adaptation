
import socket
import tkinter as tk

# create a tkinter window for the login form
window = tk.Tk()

# create widgets for the login form
username_label = tk.Label(window, text="Username:")
username_entry = tk.Entry(window)
password_label = tk.Label(window, text="Password:")
password_entry = tk.Entry(window, show="*")
submit_button = tk.Button(window, text="Submit")

# pack the widgets into the window
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
submit_button.pack()

def submit_form():
    # establish a connection to the server
    host = 'localhost'
    port = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # send the login credentials to the server
    username = username_entry.get()
    password = password_entry.get()
    message = f"{username}:{password}"
    client_socket.send(message.encode())

    # receive the response from the server
    response = client_socket.recv(1024).decode()

    # check if the user is authorized
    if response == "authorized":
        # display the file system interface
        show_file_system_interface(client_socket)
    else:
        # display an error message
        error_label = tk.Label(window, text="Invalid login credentials")
        error_label.pack()

# bind the submit button to the submit_form function
submit_button.config(command=submit_form)

def show_file_system_interface(client_socket):
    # create a new tkinter window for the file system interface
    file_system_window = tk.Toplevel()

    # create widgets for the file system interface
    label = tk.Label(file_system_window, text="Welcome to the file system interface!")
    read_write_button = tk.Button(file_system_window, text="Read/Write File", command=lambda: read_write_file(client_socket))
    quit_button = tk.Button(file_system_window, text="Quit", command=file_system_window.destroy)

    # pack the widgets into the window
    label.pack()
    read_write_button.pack()
    quit_button.pack()

def read_write_file(client_socket):
    # create a new tkinter window for the file read/write functionality
    file_window = tk.Toplevel()

    # create widgets for the file read/write window
    path_label = tk.Label(file_window, text="File Path:")
    path_entry = tk.Entry(file_window)
    text_widget = tk.Text(file_window)
    load_button = tk.Button(file_window, text="Load File", command=lambda: load_file(client_socket, path_entry.get(), text_widget))
    save_button = tk.Button(file_window, text="Save File", command=lambda: save_file(client_socket, path_entry.get(), text_widget.get("1.0", "end-1c")))
    close_button = tk.Button(file_window, text="Close", command=file_window.destroy)

    # pack the widgets into the window
    path_label.pack()
    path_entry.pack()
    text_widget.pack()
    load_button.pack()
    save_button.pack()
    close_button.pack()

def load_file(client_socket, path, text_widget):
    # send a request to the server to load the file contents
    client_socket.send(f"load:{path}".encode())

    # receive the file contents from the server
    contents = client_socket.recv(1024).decode()

    # insert the file contents into the text widget
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", contents)

def save_file(client_socket, path, contents):
    print(f"Saving file {path} with contents:\n{contents}")

    # send a request to the server to save the file contents
    client_socket.send(f"save:{path}:{contents}".encode())

    # receive the response from the server
    response = client_socket.recv(1024).decode()

    print(f"Received response from server: {response}")

    # check if the file was saved successfully
    if response == "saved":
        # display a success message
        success_label = tk.Label(text="File saved successfully")
        success_label.pack()
    else:
        # display an error message
        error_label = tk.Label(text="Error saving file")
        error_label.pack()

window.mainloop()