import json
import socket
import sys
import netifaces
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import *

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


class Server(QObject):
    newMessage = pyqtSignal(str)
    updateServer = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.server = QTcpServer()
        self.server.newConnection.connect(self.handleNewConnection)        

    def start(self):
        chosen_ip = get_local_ipv4()
        ip = QHostAddress(chosen_ip)
        port = find_open_port(chosen_ip)
        if not self.server.listen(ip, port):
            print("Failed to start server.")
            sys.exit(1)
        chosen_port = self.server.serverPort()
        # self.newMessage.emit(chosen_ip+":"+str(chosen_port))
        self.updateServer.emit(chosen_ip, chosen_port)
    
    def getIp(self):
        return self.server.serverAddress().toString()
    
    def getPort(self):
        return self.server.serverPort()

    def handleNewConnection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(self.readClientData)
        client_address = client_socket.peerAddress().toString()
        client_port = client_socket.peerPort()
        # self.newMessage.emit(f"New connection from {client_address}:{client_port}")

        

    def readClientData(self):
        client_socket = self.sender()
        data = client_socket.readAll().data().decode()
        client_address = client_socket.peerAddress().toString()
        client_port = client_socket.peerPort()
        data = data.replace("\n", "")
        self.newMessage.emit(f"{client_address}> {data}")
        response = '{status: "OK", code: 200}'
        client_socket.write(response.encode())
        client_socket.close()


       
class Client(QObject):
    newResponse = pyqtSignal(str,str,int)

    def __init__(self):
        super().__init__()

    def sendMessage(self, ip, port, message):
        success = False

        # Create a TCP socket
        client_socket = QTcpSocket()
        client_socket.connectToHost(ip, int(port))
        if client_socket.waitForConnected(1000):
            message_to_send = message #+ "\r\n"
            client_socket.write(message_to_send.encode())
            client_socket.waitForBytesWritten(1000)
            client_socket.waitForReadyRead(3000)
            response = client_socket.readAll().data().decode()

            # Convert response to JSON
            response = json.loads(response)

            if response['status'] == "OK" and response['code'] == 200:
                success = True

            # Convert response back to string before emitting the signal
            response_str = json.dumps(response)
            line =  message #f"({ip}:{port}){message}"
            self.newResponse.emit(line, response_str, response['code'])

            # Disconnect from host when ready
            client_socket.disconnected.connect(client_socket.deleteLater)
            client_socket.disconnectFromHost()

        if not success:
            self.newResponse.emit(message ,"Error: Could not send message to server.", 500)




class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intercambios")
        self.resize(600, 400)

        self.server_ip_label = QLabel("Server IP: ")
        self.server_ip_edit = QLineEdit()
        self.server_ip_edit.setReadOnly(True)
        self.server_port_label = QLabel("Server Port: ")
        self.server_port_edit = QLineEdit()
        self.server_ip_edit.setReadOnly(True)

        self.server_ip_edit.mousePressEvent = lambda event: (
            QApplication.clipboard().setText(self.server_ip_edit.text())
        )
        
        self.server_port_edit.mousePressEvent = lambda event: (
            QApplication.clipboard().setText(self.server_port_edit.text())
        )
        

        self.client_ip_label = QLabel("Client IP:")
        self.client_ip_edit = QLineEdit("192.168.")
        self.client_port_label = QLabel("Client Port:")
        self.client_port_edit = QLineEdit("8080")
        self.message_label = QLabel("Message:")
        self.message_edit = QLineEdit()
        self.send_button = QPushButton("Send")

        self.message_box = QTextBrowser()

        layout = QVBoxLayout()

        server_group_box = QGroupBox("Server")
        server_layout = QFormLayout()
        server_layout.addRow(self.server_ip_label, self.server_ip_edit)
        server_layout.addRow(self.server_port_label, self.server_port_edit)
        server_group_box.setLayout(server_layout)
        layout.addWidget(server_group_box)

        client_group_box = QGroupBox("Client")
        client_layout = QFormLayout()
        client_layout.addRow(self.client_ip_label, self.client_ip_edit)
        client_layout.addRow(self.client_port_label, self.client_port_edit)
        client_layout.addRow(self.message_label, self.message_edit)
        client_layout.addRow(self.send_button)
        client_group_box.setLayout(client_layout)
        layout.addWidget(client_group_box)

        message_group_box = QGroupBox("Conversation")
        message_layout = QVBoxLayout()
        message_layout.addWidget(self.message_box)
        message_group_box.setLayout(message_layout)
        layout.addWidget(message_group_box)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.sendMessage)


    def updateServerInfo(self, host, port):
        # self.server_info_label.setText(f"{host}:{port}")
        self.server_ip_edit.setText(f"{host}")
        self.server_port_edit.setText(f"{port}")

    def showMessage(self, message):
        self.message_box.append(message)



    def sendMessage(self):
        ip = self.client_ip_edit.text()
        port = self.client_port_edit.text()
        message = self.message_edit.text()

        if ip and port and message:
            client = Client()
            client.newResponse.connect(self.handleResponse)
            client.sendMessage(ip, port, message)

        else:
            QMessageBox.warning(self, "Error", "Please enter the IP, port, and message.")

    def handleResponse(self,message, status,code):
        if code == 200:
            self.showMessage(f"{message}")
        else:
            self.showMessage(f"❌: {message}")

        # Delete the client instance after handling the response
        client = self.sender()
        client.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = Server()

    window = ServerWindow()
    window.show()

    server.newMessage.connect(window.showMessage)
    server.updateServer.connect(window.updateServerInfo)

    server.start()

    sys.exit(app.exec_())
