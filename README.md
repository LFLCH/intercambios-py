```
  _____           _                                              _       _               
 |_   _|         | |                                            | |     (_)              
   | |    _ __   | |_    ___   _ __    ___    __ _   _ __ ___   | |__    _    ___    ___ 
   | |   | '_ \  | __|  / _ \ | '__|  / __|  / _` | | '_ ` _ \  | '_ \  | |  / _ \  / __|
  _| |_  | | | | | |_  |  __/ | |    | (__  | (_| | | | | | | | | |_) | | | | (_) | \__ \
 |_____| |_| |_|  \__|  \___| |_|     \___|  \__,_| |_| |_| |_| |_.__/  |_|  \___/  |___/
```
<b>Intercambios is a local network messaging system.</b><br>
It aims to connect devices of different types so that they can easily exchange data with each other.
It is currently based on TCP sockets. 

# intercambios-py
This repository contains the code of the Python scripts that are part of the Intercambios project.

## File structure
```
.
├── 📜 app.py
├── 📜 basic_server.py
├── 📜 client.py
├── 📜 qr_code.py
└── 📜 server.py
```
### _app.py_
It is the entypoint of the application. Running it provides a GUI that allow the interaction with the local network.<br>
It uses the Qt framework to do so.

![capture of the application](https://github.com/LFLCH/intercambios-py/assets/62034725/ac3e55f6-2ff3-4ec7-a479-81853550f089)

### _basic_server.py
It helped understanding how TCP socket server work. Its main disadvantage is that it blocks access to the console started (even ctrl+c does not work).

### _server.py_ && _client.py_
These scripts can be run independently, they provide a TCP client/server. Their output are in the console, and they can be stopped using ctrl+c signal.  
