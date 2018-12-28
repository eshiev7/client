import socket 
import time

class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout = 15):
        try:
            self.sock = socket.create_connection((host, port), timeout)
        except:
            raise ClientError("Error")
            
    def put(self, key, value, timestamp = int(time.time())):
        try:
            self.sock.sendall(("put " + str(key) + " " + str(value) + " " + str(timestamp) + "\n").encode())
            data = self.sock.recv(1024)
        except  :
            raise ClientError("Error")
        if data.decode() == "ok\n\n":
                pass
        else:
            raise ClientError("Error")
            
    def get(self, key):
        dictionary = dict()
        try:
            self.sock.sendall(("get " + str(key) + "\n").encode())
            metrics = self.sock.recv(1024).decode()
        except:
            raise ClientError("Error")
        if metrics == "error\nwrong command\n\n":
            raise ClientError("Error")
        elif metrics == "ok\n\n":
            pass
        metrics = metrics.replace("\n\n", "").replace("ok\n", "").split("\n")
        for i in metrics:
            if len(i.split()) == 3:
                if i.split()[0] in dictionary:
                    dictionary[i.split()[0]].append((int(i.split()[2]),float(i.split()[1])))
                else:
                    dictionary[i.split()[0]] = [(int(i.split()[2]),float(i.split()[1]))]
        return dictionary
