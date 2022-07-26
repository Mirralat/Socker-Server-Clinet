import socket
import asyncio
from Socket import Socket
from datetime import datetime
from os import system
 
# the chat for a very lonely person 
# without encryption and GUI
# completed and debugged
 
class Socket:
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )  # TCP/IP
        self.main_loop = asyncio.new_event_loop()   # single loop
 
    async def send_data(self, data=None):
        raise NotImplementedError()
 
    async def listen_socket(self, listened_socket=None):
        raise NotImplementedError()
 
    async def main(self):
        raise NotImplementedError()   # if no-async
 
    def start(self):
        self.main_loop.run_until_complete(self.main())
 
    def set_up(self):
        raise NotImplementedError()
 
class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
 
        self.users = []
 
    def set_up(self):
        self.socket.bind(("127.0.0.1", 5000))
        self.socket.listen(5)
        self.socket.setblocking(False)  # non-blocking
        print('Server is listening')
 
    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)
 
    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return
        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)  # bytes
                await self.send_data(data)
 
            except ConnectionResetError:
                print("Client removed!")
                self.users.remove(listened_socket)
                return
 
    async def accept_sockets(self):
        while True:
            u_socket, address = await self.main_loop.sock_accept(self.socket)  # connected
            print(f"User <{address[0]}> connected!")
 
            self.users.append(u_socket)
            self.main_loop.create_task(self.listen_socket(u_socket))
 
    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())
 

if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()  # main loop
