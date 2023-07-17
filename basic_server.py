import socket

# This script is the script of a BLOCKING program that awaits for 1 request only
###################################
#          IMPORTANT              #
#    YOU NEED TO ALLOW PYTHON     #
# IN THE FIREWALL TO MAKE IT WORK #
#       ON THE LOCAL NETWORK      # 
###################################


# Create a socket object
host = "192.168.XX.YY" #write down the ip address
port = 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}...")

client_socket, client_address = server_socket.accept()
print(f"Connected to client: {client_address[0]}:{client_address[1]}")
# Receive data from the client
data = client_socket.recv(1024).decode("utf-8")
print(f"Received data: {data}")

# Process the data or perform any desired operations

# Send a response back to the client
response = '{"status":"OK"}'
client_socket.send(response.encode('utf-8'))

# Close the client socket
client_socket.close()
#Close the server socket
server_socket.close()
print("Server closed")
         