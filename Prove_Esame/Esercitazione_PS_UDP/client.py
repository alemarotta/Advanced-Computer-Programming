import sys,random,time
import threading as mt
from proxy import Proxy
def run_func(nr,richiesta,port):
    articolo=["laptop","smartphone"]
    time.sleep(random.randint(2,4))
    proxy = Proxy(int(port))
    for i in range(3):
        print(f"[CLIENT] Sto generando la richiesta nr {str(i)} per il thread nr. {str(nr)}")
        if richiesta=="deposita":
            selected_articolo=articolo[random.randint(0,1)]
            id_selected=random.randint(1,100)
            proxy.deposita(selected_articolo,id_selected)
            message_client=selected_articolo+"-"+str(id_selected)
            print("[CLIENT] Ho generato una richiesta di deposita con: ",message_client)
            
        elif richiesta=="preleva":
            selected_articolo=articolo[random.randint(0,1)]
            proxy.preleva(selected_articolo)
            print("[CLIENT] Ho generato una richiesta di preleva con seguente articolo: ",selected_articolo)
        
            
        
    

if __name__=="__main__":
    try:
        port=sys.argv[1]
        richiesta=sys.argv[2]
    except IOError:
        print("[CLIENT] Inserisci di nuovo")
    
    threads=[]
    for i in range(5):
        th=mt.Thread(target=run_func,args=(i,richiesta,port))
        th.start()
        print(f"[CLIENT] Thread nr {str(i)} startato")
        threads.append(th)
        
    for thread in threads:
        thread.join()