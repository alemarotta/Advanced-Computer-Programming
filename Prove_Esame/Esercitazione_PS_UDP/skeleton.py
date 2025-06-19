from interface import Interface
import socket
import threading as mt

def run_func(socket,addr,messageClient,skeleton):
    response=messageClient.decode("utf-8")
    print("[SKELETON] Ho ricevuto la seguente richiesta: ",response)
    richiesta=response.split("-")[0]
    message_to_send="ACK"
    if richiesta=="deposita":
        articolo=response.split("-")[1]
        id=response.split("-")[2]
        skeleton.deposita(articolo,int(id))
        socket.sendto(message_to_send.encode("utf-8"),addr)
        
    else:
        articolo=response.split("-")[1]
        skeleton.preleva(articolo)
        socket.sendto(message_to_send.encode("utf-8"),addr)
        
        
            
class Skeleton(Interface):
    def __init__(self, host,port,delegate):
        self.host=host
        self.port=port
        self.delegate=delegate
        self.buffer_size=1024
        
    def deposita(self, articolo, id):
        self.delegate.deposita(articolo,id)
        
    def preleva (self,articolo):
        self.delegate.preleva(articolo)
        
    def run_Skeleton(self):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            s.bind((self.host,self.port))
            port=s.getsockname()[1]
            print("[SKELETON] Sono in ascolto su porto: ",str(port))
            while True:
                response,addr=s.recvfrom(self.buffer_size)
                
                th=mt.Thread(target=run_func,args=(s,addr,response,self))
                th.start()