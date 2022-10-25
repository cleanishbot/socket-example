import selectors
import socket


class Listener:
    def __init__(self, host='127.0.0.1', port=5678, no_conns=5):
        self.keep_running = True
        self.server_address = (host, port)
        self.no_conns = no_conns

    def open_socket(self):
        print(f'Starting the socket on {self.server_address[0]}:{self.server_address[1]}')
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.socket.setblocking(False)
        self.socket.bind(self.server_address)
        self.socket.listen(self.no_conns)

    def register_selector(self):
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.socket, selectors.EVENT_READ, self.on_accept)

    def on_accept(self, sock, mask):
        print('New connection')
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read_from_conn)
    
    def read_from_conn(self, conn, mask):
        print('Reading from the conn')
        data = conn.recv(1024)

        if data:
            print('Received {!r}'.format(data))
            conn.sendall(data)
        else:
            print('Closing connection')
            self.sel.unregister(conn)
            conn.close()
            self.keep_running = False

    def start(self):
        self.open_socket()
        self.register_selector()
        self.main_loop()

    def main_loop(self):
        print('waiting for I/O')
        for key, mask in self.sel.select(timeout=1):
            callback = key.data
            callback(key.fileobj, mask)

        if self.keep_running:
            self.main_loop()
        else:
            self.end()

    def end(self):
        print('Shutting down')
        self.sel.close()
        self.socket.close()
        print('Complete')

l = Listener()
l.start()
