import selectors
import socket


class Client:
    def __init__(self, host='127.0.0.1', port=5678):
        self.server_address = (host, port)
        self.keep_running = True
        self.conn = None
        self.messages = [
            b'This is a message',
            b'It could have been sent',
            b'Who knows'
        ]

    def open_socket(self):
        print(f'Starting the socket on {self.server_address[0]}:{self.server_address[1]}')
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.socket.connect(self.server_address)
        self.socket.setblocking(False)
    
    def register_selector(self):
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.socket, selectors.EVENT_READ | selectors.EVENT_WRITE,)

    def read_from_conn(self):
        print('Reading:')
        data = self.conn.recv(1024)
        if data:
            print('    {!r}'.format(data))
            print('Recieved {} bytes'.format(len(data)))
        else:
            print('    No data.')
            self.keep_running = False
    
    def get_next_msg(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)
        return None

    def write_to_conn(self, msg=None):
        print('Ready to write')
        if msg:
            self.send_msg(msg)
        else:
            print('Switching to read-only')
            self.sel.modify(self.socket, selectors.EVENT_READ)

    def send_msg(self, msg):
        print('Sending msg:')
        print('    {!r}'.format(msg))
        self.socket.sendall(msg)
        print('Sent {} bytes'.format(len(msg)))

    def start(self):
        self.open_socket()
        self.register_selector()
        self.main_loop()

    def main_loop(self):
        print('Waiting for I/O')

        for key, mask in self.sel.select(timeout=1):
            self.conn = key.fileobj

            if mask & selectors.EVENT_READ:
                self.read_from_conn()
            elif mask & selectors.EVENT_WRITE:
                self.write_to_conn(self.get_next_msg())

        if self.keep_running:
            self.main_loop()
        else:
            self.end()

    def end(self):
        print('Shutting down')
        if self.conn:
            self.sel.unregister(self.conn)
            self.conn.close()
        self.sel.close()
        self.socket.close()
        print('Complete')

c = Client()
c.start()
