import asyncio
import netifaces 
import socket

# This script is a script of a non-blocking server 
# It uses methods from the asyncio library, instead of sockets ones
# The socket library is only used for the automation of port finding


# Automatically find the ip of the network (192.168.XX.XX)
# In Windows, requires the installation of Visual Studio Build Tools
def get_local_ipv4():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET]
    interface = default_gateway[1]  

    addresses = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addresses:
        ip_info = addresses[netifaces.AF_INET][0]
        local_ip = ip_info['addr']
        return local_ip
    return "0.0.0.0"

# Automatically finding an available port
# First checks pre-defined ports for a stability sake
def find_open_port(host, traditional_ports=[8080]):
    for port in traditional_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.close()
            return port
        except OSError:
            pass

    # No traditional port has been found
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, 0)) 
    _, port = sock.getsockname()
    sock.close()
    return port
        

async def handle_client(reader, writer):
    # Receive data from the client
    data = await reader.read(1024)
    message = data.decode("utf-8")
    print(f"{writer.get_extra_info('peername')[0]}>{message}")


    # Send a response back to the client
    response = '{"status":"OK", "code":200}'
    writer.write(response.encode('utf-8'))
    await writer.drain()

    # Close the client connection
    writer.close()

async def start_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr[0]}:{addr[1]}...")
    
    await server.serve_forever()


def main():
    # Create a socket object
    host = get_local_ipv4()
    port = find_open_port(host)
    
    try:
        asyncio.run(start_server(host, port))
    except KeyboardInterrupt:
        print("Server stopped by user")
         

if __name__ == "__main__":
    main()

