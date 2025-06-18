import stomp
import random,sys,time
import threading as mt
class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print("[OPERATOR] Ho ricevuto la seguente risposta: ",frame.body)
        
    

def run_thread(conn,i,operator):
    client=["Superman","Batman","Spiderman","Flash"]
    richiesta=["CREATE","UPDATE"]
    if i<4:
        nights=random.randint(1,30)
        people=random.randint(1,8)
        cost=random.randint(50,300)
        
        MSG=richiesta[0]+"-"+client[i]+"-BudapestHotel-"+operator+"-"+str(nights)+"-"+str(people)+"-"+str(cost)
        conn.send("/topic/request",MSG)
        print("[OPERATOR] Ho inviato la seguente richiesta: ",MSG)
    else:
        discount=random.randint(20,100)
        nights=random.randint(1,30)
        MSG=richiesta[1]+"-"+operator+"-"+str(discount)+"-"+str(nights)
        conn.send("/topic/request",MSG)
        print("[OPERATOR] Ho inviato la seguente richiesta: ",MSG)



if __name__=="__main__":
    try:
        OPERATOR = sys.argv[1]
    except IOError:
        print("[OPERATOR] Riscrivi l'operatore grazie")
    
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.set_listener("",MyListener())
    conn.connect(wait=True) 
    conn.subscribe("/topic/response",id=1,ack='auto') 
    threads=[]
    for i in range(6):
        th=mt.Thread(target=run_thread,args=(conn,i,OPERATOR))
        th.start()
        threads.append(th)
    
    for thread in threads:
        thread.join()   
    
    
    time.sleep(60)
    conn.disconnect()
          
        
        