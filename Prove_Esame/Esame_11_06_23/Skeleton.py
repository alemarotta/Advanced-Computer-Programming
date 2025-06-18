from IPrinter import IPrinter
from abc import ABC,abstractmethod
import socket
import multiprocessing as mp
import stomp
def prod_func(conn,skeleton):
    message=conn.recv(1024).decode("utf-8")
    print("[SKELETON] Ho ricevuto il seguente messaggio: ",message)
    
    pathfile= message.split("-")[1]
    tipo=message.split("-")[2]
    skeleton.print(pathfile,tipo)
    response="ACK"
    conn.send(response.encode("utf-8"))
    print("[SKELETON] Ho inviato la risposta")
    conn.close()
    
def consum_func(skeleton):
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.connect(wait=True)
    ##while True:        
    message=skeleton.consuma()
    print("[SKELETON] Ho consumato il seguente messaggio: ",message)
    color=message.split("-")[1]
    if color == "color":
        conn.send("/queue/color",message)
    else:
        conn.send("/queue/bw",message)
    
    print("[SKELETON] Inviato nella stomp queue")
    
class Skeleton(IPrinter,ABC):
    def __init__(self,host,port):
        self.host=host
        self.port=port
    
    @abstractmethod 
    def print(self, pathFile, tipo):
        pass
    
    
    def run_Skeleton(self):
        sck=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sck.bind((self.host,self.port))
        print("[SKELETON SERVER] Sto in ascolto su porto: ",str(sck.getsockname()[1]))
        sck.listen(30)
        while True:
            c,addr=sck.accept()
            
            p = mp.Process(target = prod_func,args=(c,self))
            p.start()
            
            co=mp.Process(target=consum_func,args=(self,))
            co.start()
        sck.close()