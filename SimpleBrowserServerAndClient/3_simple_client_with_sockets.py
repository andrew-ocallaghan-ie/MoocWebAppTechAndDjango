import socket

"""
While simple_server is running, you can hit it with this client.
in one terminal run python3 2_simple_server.py
in another use this client python3 3_simple_client_with_sockets
You'll see hello world is returned and in the server logs you'll see the request was made.
"""

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9000))
CMD = "GET http:/127.0.0.1/romeo.txt HTTP/1.0\r\n\r\n".encode()
client_socket.send(CMD)
while True:
    response_data = client_socket.recv(512)
    if len(response_data)<1:
        break
    print(response_data.decode(), sep='')
