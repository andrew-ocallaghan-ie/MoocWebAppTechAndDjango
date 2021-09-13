from socket import *

"""
This example opens a socket that listens to localhost port 9000.
It can respond to 1 call and queue up another 4.
It continuously trys to accept incoming requests and blocks execition until it does.
Once it recieves a request it prints it and replies with encoded Hello World Html

After execution you may wish to kill a process if a resource is hanging.
ps -fA | grep python
kill -9 <PID>
"""

def createServer():
    server_socket = socket(AF_INET, SOCK_STREAM) #make socket to recieve client message
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #hack to let server re-run without address
    try:
        server_socket.bind(('localhost', 9000)) #this program consumes port 9000
        server_socket.listen(5) #Queue 4 more calls if this socket is busy

        # keep serving many requests until execution is ended via error or interrupt
        while True:

            #this is a blocking call
            #code will NOT proceed any further until there is something to accept.
            client_socket, address = server_socket.accept()

            #after something has been accepted, proceed to parse, log and respond.
            request_data = client_socket.recv(5000).decode().split("\n")
            if len(request_data) > 0:
                for line in request_data:
                    print(line)

            # construct response
            data = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
            data += "<html><body>Hello World</body></html>\r\n\r\n"

            # send encoded response and shutdown connection.
            client_socket.sendall(data.encode())
            client_socket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print("\nShutting down..\n")

    except Exception as e:
        print("Error:\n")
        print(e)

    # cleanup the socket when function is closing.
    server_socket.close()

#print convinient url to terminal
print('Access http://localhost:9000')
createServer()
