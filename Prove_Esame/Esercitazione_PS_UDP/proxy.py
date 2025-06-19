from interface import Interface
import socket

class Proxy(Interface):
    def __init__(self,port):
        self.host="localhost"
        self.port=port
        self.buffer_size=1024
    
    def deposita(self, articolo, id):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            message_to_send="deposita-"+articolo+"-"+str(id)
            print("[PROXY] Sto inviando: ",message_to_send)
            s.sendto(message_to_send.encode("utf-8"),(self.host,self.port))
            response,address=s.recvfrom(self.buffer_size)
            print("[PROXY] Ho ricevuto la seguente risposta alla richiesta deposita: ",response.decode("utf-8"))
        
    def preleva(self, articolo):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            message_to_send="preleva-"+articolo
            print("[PROXY] Sto inviando:",message_to_send)
            s.sendto(message_to_send.encode("utf-8"),(self.host,self.port))
            response,address=s.recvfrom(self.buffer_size)
            print("[PROXY] Ho ricevuto la seguente risposta all richiesta di preleva: ",response.decode("utf-8"))
        