import os
import platform
import socket
import threading
if platform.system().startswith("Windows"):
    try:
        from pystyle import *
    except ImportError:
        os.system("python -m pip install pystyle -q -q -q")
        from pystyle import *
elif platform.system().startswith("Linux"):
    try:
        from pystyle import *
    except ImportError:
        os.system("python3 -m pip install pystyle -q -q -q")
        from pystyle import *

banner = Center.XCenter(r"""
*****************************************************************************
*     ____  __ _   _ _   _____ ___ _   _ _____ _____ ____    _  _______     *
*    / /  \/  | | | | | |_   _|_ _| \ | | ____|_   _/ ___|  / \|_   _\ \    *
*   | || |\/| | | | | |   | |  | ||  \| |  _|   | || |     / _ \ | |  | |   *
*  < < | |  | | |_| | |___| |  | || |\  | |___  | || |___ / ___ \| |   > >  *
*   | ||_|  |_|\___/|_____|_| |___|_| \_|_____| |_| \____/_/   \_\_|  | |   *
*    \_\                                                             /_/    *
*                       CROSS PLATFORM MULTI NETCAT SERVER                  *
*                              Coded By: Machine1337                        *
*****************************************************************************                        
""")
os.system("cls||clear")
print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
class Client:
    def __init__(self, connection, address, client_id):
        self.connection = connection
        self.address = address
        self.client_id = client_id
        self.data_received = False

    def handle(self):
        while True:
            if self.data_received:
                try:
                    data = self.connection.recv(4096)

                    if not data:
                        break

                    print(data.decode(), end='')
                except ConnectionResetError:
                    break
                except KeyboardInterrupt:
                    break

        #self.connection.close()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.client_id = 0
    def start(self):
        print(f"[+] Listening on {self.host} {self.port}\n")
        while True:
            connection, address = self.server_socket.accept()
            print(Colors.green+f"\n[*] Connection received on {address[0]} {address[1]}\n[*] SERVER COMMAND: ", end='')
            client = Client(connection, address, self.client_id)
            self.clients.append(client)
            self.client_id += 1
            client_thread = threading.Thread(target=client.handle)
            client_thread.start()
    def show_clients(self):
        print(Colors.cyan+"\n[*] Connected clients:")
        for client in self.clients:
            print(f"ID: {client.client_id}, IP: {client.address[0]}, Port: {client.address[1]}")
        print("", end='')

    def shell(self, client_id):
       try:
           for client in self.clients:
               if client.client_id == client_id:
                   print(Colors.yellow + f"[*] Connected to client {client_id}")
                   client.data_received = True
                   while True:
                       command = input("")
                       if command == "back":
                           os.system("cls||clear")
                           print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
                           self.server_commands()
                       elif command == "clear":
                           os.system("cls||clear")
                           print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
                       client.connection.send(command.encode() + b"\n")
                       print(f"[*] Sent command: {command}")
                   break
           else:
               print("[-] Client not found\n", end='')
       except:
           print(Colors.red + "\n[-] Ctrl+C Detected .......")
           exit(1)
    def server_commands(self):
        try:
            while True:
                command = input(Colors.green + "[*] SERVER COMMAND: ")
                if command.lower() == "exit":
                    break
                elif command == "list":
                    os.system("cls||clear")
                    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
                    self.show_clients()
                elif command == 'help':
                    os.system("cls||clear")
                    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
                    print(Colorate.Vertical(Colors.red_to_purple, """
                                 ****  SERVER COMMANDS MAIN MENU ****

                        1. id 0    | Entering current shell
                        2. list    | Show Connected Clients
                        3. back    | Back To The Server Main Menu 
                                       More Features Will Be Added
                                       Follow:- github.com/machine1337
                                                    """, 2))
                elif command == "clear":
                    os.system("cls||clear")
                    print(Colorate.Vertical(Colors.green_to_yellow, banner, 2))
                elif command.startswith("id "):
                    client_id = int(command.split()[1])
                    self.shell(client_id)
        except:
            print(Colors.red+"\n[-] Ctrl+C Detected .......")
            exit()

if __name__ == "__main__":
    try:
        server = Server("0.0.0.0", 9999)
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
        server.server_commands()
    except KeyboardInterrupt:
        print(Colors.red+"\n[-] Ctrl+C Detected......")
        server.stop()
        exit(1)
