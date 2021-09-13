import urllib.request

"""
Wheras previously we used sockets, now we'll use URL lib, which focuses on HTTP requests
Under the hood we'll still be using sockets.
"""

file_handle = urllib.request.urlopen('http://127.0.0.1:9000/romeo.txt')
for line in file_handle:
    print(line.decode().strip())
