import socket

host = '127.0.0.1'
port = 5678

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.bind((host, port))
sock.listen(1) # max 1 connection

# Blocks until a client connection is accepted
conn, addr = sock.accept()
print("CONNECTION FROM:", str(addr))

conn.send(b'Some message to send to the client')

msg = "Another message, but this time not originally in binary"
conn.send(msg.encode())

# Disconnect the client
conn.close()
