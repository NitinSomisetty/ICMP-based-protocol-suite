import argparse
import asyncio
from ssl_utils import create_client_ssl_context


def parse_args():
    parser = argparse.ArgumentParser(description="TLS diagnostic client")
    parser.add_argument("--server-host", default="127.0.0.1", help="Server IP or hostname")
    parser.add_argument("--server-port", type=int, default=8888, help="Server TCP port")
    return parser.parse_args()


async def main(server_host, server_port):

    host = input("Enter target host: ")

    ssl_context = create_client_ssl_context()

    reader, writer = await asyncio.open_connection(
        server_host,
        server_port,
        ssl=ssl_context
    )

    writer.write(host.encode())
    await writer.drain()
 
    data = await reader.read(10000)

    print("\nSERVER RESPONSE\n")
    print(data.decode())

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.server_host, args.server_port))