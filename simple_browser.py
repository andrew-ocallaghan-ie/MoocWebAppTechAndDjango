import socket
import ssl

"""
Sockets : Combining Application, Presentation, Session layer (7,6,5)
Sockets allow bidirectional communication between application processes over an IP based network.
Not just inter-server communication, its more granular, inter-process communication across a network.
Inter-server would be from IP-IP, whereas inter-process is IP:port-Ip:port
Recall ports are just different endpoints on a server that independently send and recieve traffic.

Sockets let us consider two processes as being in direct communication with each other even though they are separated
by many nodes across the internet.

IP - Network Layer (3)
Recall two distant nodes communicate using IP (internet protocol).
- routing algorithm is used to build a forwarding table on each node in the network.
- The forwarding tables map ip-ranges their neighboring nodes so they know where to best redirect messages.

TCP - Transport Layer (4)
The connection between source and dest in a socket is setup and torn down via TCP (which uses IP).
- A 3-way handshake is performed to setup connection. (sync, syn-ack, ack)
- 4 way disconnect is used to teardown connection (fin, finack, fin, finack )
- or a hard TCP reset to quickly hangup without acks (reset)

DNS Resolution - Application Layer (7)
Recall also that the host in a URL resolve to an IP address via a DNS lookup. It uses TCP and UDP both which use IP.
The IP can be resolved recursively using a DNS resolver server, or iteratively.

data.pr4e.org or www.example.com are examples of domains, see how they are parsed below.
{sub-domain}    {root-domain}   {top-level-domain}
www             example         com
data            pr4e            org

DNS Recursive
client queries resolver for www.example.com, resolver issues heirachial queries to resolve host IP.
resolver queries www.example.com to root server, which replies try com server at xx.xx.xx.xx
resolver sends www.example.com to .com server, which replies try example.com server at yy.yy.yy.yy
resolver sends www.example.com to example.com server, which replies try www.example.com server at zz.zz.zz.zz
resolver sends www.example.com to www.example.com server which replies with 12.34.56.78
The resolver then caches the domain ip address mapping and sends it to client.
The caching makes request faster and reduces pressure on name servers.
But the cache can be poisoned creating a security vunerability

DNS Iterative
The client doesn't delegate to the resolver, it heirachially queries the DNS name servers directly in the same manner.
This is more secure; its not vunderable to DNS cache poisoning. But its slower and puts pressure on name servers.

Browsers :
Browsers (a client) that uses a socket to make requests to servers for data. It can use different protocols.
The browser needs a URL, so it can use different protocols to get documents from a domain.

The resource being retrieved is represented as a URL (uniform resource locator)
http://     data.pr4e.org   /page.htm
{protocol}  {domain}        {document}

The domain resolves to an IP address via DNS. The document is an actual document within the server.
The server returns the document (text, html, an image) and some metadata/header info for it (size, type, http status)

Modern browsers with a GUI render/paints the page and have event looks so users can interact with document.
If the browser was very thin, it would just return the file and headers to user. Such as the one below.
"""

def browser(protocol='http', protocol_version='1.0', host='', document=''):
    # AF_INET -> Address Family for Internet IPv4
    # A pair(host, port) is used for the AF_INET address family,
    # where host is a string representing either a hostname in Internet domain.
    # e.g.'daring.cwi.nl' or an IPv4 address like '100.50.200.5'
    # port is an integer.Used to communicate between processes over the Internet.
    # e.g. 80, or 443

    # SOCK_STREAM is connection based, it uses TCP
    # another type is SOCK_DGRAM which uses datagrams - UDP

    base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    base_socket.settimeout(2)
    browser_socket =  ssl.wrap_socket(base_socket) if protocol == 'https' else base_socket

    port = 443 if protocol == 'https' else 80
    address = (host, port)
    browser_socket.connect(address)

    # e.g. http://data.pr4e.org/page1.htm
    url = f'{protocol}://{host}{document}'
    request = f'GET {url} HTTP/{protocol_version}\r\n\r\n'.encode()
    browser_socket.send(request)

    while True:
        try:
            data = browser_socket.recv(512)
            if len(data) < 512:
                break
            print(data.decode(), end='')
        except socket.timeout:
            break

    browser_socket.close()


if __name__ == '__main__':
    browser(host='data.pr4e.org', document='/page1.htm')
    browser(protocol='http', protocol_version='1.0', host='google.com', document='/')
    browser(protocol='https', protocol_version='1.1', host='google.com', document='/')
