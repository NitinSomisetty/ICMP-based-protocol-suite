import ssl
# on top of sockets, adding encryption.
# socket -> ssl.wrap -> encrypted communication

def create_server_ssl_context(): # for server side, we need to load the certificate and private key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH) 
#An SSL context object is a Python object that stores all TLS/SSL settings for secure connections.
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context
 # So traffic is encrypted, but the client does not authenticate the server identity

def create_client_ssl_context(): 
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE # accepts any certificate, even if it's self-signed or invalid.
    return context