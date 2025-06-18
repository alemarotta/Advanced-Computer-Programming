import socket
from IPrinter import IPrinter
class Proxy(IPrinter):
    def __init__(self,port):
        self.port=port
        self.host="localhost"
        self.bufsize=1024
    
    def print(self,pathFile,tipo):
        sck=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sck.connect((self.host,int(self.port)))
        
        message = "print-"+pathFile+"-"+tipo
        print("[PROXY] Ho generato la seguente richiesta: ",message)
        sck.send(message.encode("utf-8"))
        print("[PROXY] Ho inviato la richiesta")
        
        response=sck.recv(self.bufsize).decode("utf-8")
        print("[PROXY] Ho ricevuto la seguente risposta: ",response)
        sck.close()