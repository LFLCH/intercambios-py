import socket

def main():
    # Replace "SERVER_IP" with the actual IP address of the server
    server_ip = "192.0.XX.YY"
    port = 8080

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_ip, port))
        print("Connected to server:", server_ip)

        
        # Send a message to the server
        message = "Bliblou 😸"
        client_socket.sendall(message.encode())
        print("Data has beeen sent")

        # Receive the response from the server
        response = client_socket.recv(1024).decode()
        print("Received response:", response)
        

        # Close the socket connection
        client_socket.close()
        print("End")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running and the IP address is correct.")

if __name__ == "__main__":
    main()
