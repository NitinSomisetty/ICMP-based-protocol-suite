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

    # writer.get_extra_info("peername")   # remote (IP, port)
    # writer.get_extra_info("sockname")   # local (IP, port)
    # writer.get_extra_info("socket")     # raw socket object
    # writer.get_extra_info("ssl_object") # SSL/TLS info (if using SSL)

    if ssl_obj:
        print("SSL connection established")
        print("Cipher: ", ssl_obj.cipher())

    data = await reader.read(1024) #after user enters host name
    host = data.decode().strip()

    print(f"Request for: {host}")

    ip = resolve_host(host)

    if not ip:
        writer.write(b"Host resolution failed")
        await writer.drain()
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


async def main():

    ssl_context = create_server_ssl_context()

    server = await asyncio.start_server(
        handle_client, #that up function
        "0.0.0.0", #listen on all interfaces
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

