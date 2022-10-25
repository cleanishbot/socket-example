import socket

host = '127.0.0.1'
port = 5678

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.connect((host, port))

msg = sock.recv(1024)

# Read the whole message
while msg:
    print('Received:' + msg.decode())
    msg = sock.recv(1024)
 
sock.close()
