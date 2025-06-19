from interface import Interface
import stomp,socket
import multiprocessing as mp
from abc import ABC
def prod_func(conn,skeleton):
    response=conn.recv(1024).decode("utf-8")
    print("[SKELETON] Messaggio ricevuto:",response)
    messaggio=response.split("-")[0]
    tipo=response.split("-")[1]
    skeleton.log(messaggio,int(tipo))
    message_to_send="ACK"
    conn.send(message_to_send.encode("utf-8"))
    conn.close()

def consum_func(skeleton):
    connection=stomp.Connection([("127.0.0.1","61613")])
    connection.connect(wait=True)
    response=skeleton.consuma()
    tipo=response.split("-")[1]
    if int(tipo)==2:
        print("[SKELETON] Sto inviando nella queue error")
        connection.send("/queue/error",response)
    else:
        print("[SKELETON] Sto inviando nella queue info")
        connection.send("/queue/info",response)
    
    connection.disconnect()
    
    
class Skeleton(Interface,ABC):
    def __init__(self):
        self.host="localhost"
        self.port=0
        self.buf_size=1024
    
    def log(self, messaggio, tipo):
        pass
    
    def run_skeleton(self):
        
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind((self.host,self.port))
            s.listen(30)
            port=s.getsockname()[1]
            print("[SKELETON] Sono in ascolto su porto:",str(port))
            
            while True:
                conn,addr=s.accept()
                p=mp.Process(target=prod_func,args=(conn,self))
                p.start()
                
                c=mp.Process(target=consum_func,args=(self,))
                c.start()
                
                
                
                