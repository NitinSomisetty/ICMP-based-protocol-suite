import socket

def resolve_host(host):
    try:
        return socket.gethostbyname(host) # does dns lookup and returns ip address
    except socket.gaierror:
        return None