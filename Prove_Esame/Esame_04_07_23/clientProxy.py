import socket
from interface import Interface
class ClientProxy(Interface):
    def __init__(self,port):
        self.host="localhost"
        self.port=port
        self.buf_size=1024
        
    def log(self, messaggio, tipo):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((self.host,int(self.port)))
            data=messaggio+"-"+str(tipo)
            print("[PROXY] Sto inviando la seguente richiesta:",data)
            s.send(data.encode("utf-8"))
            messagge_received=s.recv(self.buf_size).decode("utf-8")
            print("[PROXY] Messaggio ricevuto:",messagge_received)
            
            
            