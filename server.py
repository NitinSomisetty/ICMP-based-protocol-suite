import asyncio
from ping import ping 
from traceroute import traceroute
from utils import resolve_host
from ssl_utils import create_server_ssl_context


async def handle_client(reader, writer):  # reader and writer wrap tcp sockets

    addr = writer.get_extra_info("peername") #the other side of the connection (remote server's)
    #addr has ip and port of the other connection -> metadata 

    print(f"Client connected: {addr}")
    ssl_obj = writer.get_extra_info("ssl_object")

    # writer.get_extra_info("peername")   # remote client (IP, port)
    # writer.get_extra_info("sockname")   # local (IP, port) the servers
    # writer.get_extra_info("socket")     # raw socket object
    # writer.get_extra_info("ssl_object") # SSL/TLS info (if using SSL)

    if ssl_obj:
        print("SSL connection established")
        print("Cipher: ", ssl_obj.cipher()) #Server can inspect negotiated TLS details via ssl_object/cipher 

    data = await reader.read(1024) #after user enters host name
    """
    reader is the input stream for the TCP connection
    reader -> recieve side
    writer -> send side

    """ 
    host = data.decode().strip().lower()

    print(f"Request for this Host: {host}")

    ip = resolve_host(host)

    if not ip:
        writer.write(b"Host resolution failed")
        await writer.drain() #Waits until the stream buffer flushes enough to safely continue.
        writer.close()
        return

    ping_result = ping(host)  # await call
    trace = traceroute(host)

    response = " -- PING RESULTS -- \n"
    response += ping_result + "\n"

    response += " -- TRACEROUTE -- \n"

    for hop in trace:
        response += hop + "\n"

    writer.write(response.encode())
    await writer.drain()  #Waits until the stream buffer flushes enough to safely continue. 
    print(f"Response sent successfully for: {host}\n")
    writer.close()
    await writer.wait_closed()


async def main():  #main function to set up the server and listen for incoming connections

    ssl_context = create_server_ssl_context()

    server = await asyncio.start_server( #Start a socket server, call back for each client connected
        handle_client, # that above function, its a callback
        "0.0.0.0", # listen on any ip address
        8888,
        ssl=ssl_context
    )

    print("Diagnostic Server Running on port 8888\n")

    async with server:
        await server.serve_forever() #runs the server indefinitely, handling incoming connections

asyncio.run(main())
#This is the program entry point. It creates an event loop, runs main(), 
# and keeps the application alive until main finishes, 
# which here means essentially forever unless interrupted.

