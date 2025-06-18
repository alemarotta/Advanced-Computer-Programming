import sys,grpc,random,service_pb2,service_pb2_grpc
import threading as mt
def run_thread(number_thread,port):
    with grpc.insecure_channel("localhost:"+port) as channel:
        stub=service_pb2_grpc.ProductMaanagerStub(channel)
        if number_thread%2==0:
            print("[USER] Ho inviato una richiesta di buy")
            response=stub.buy(service_pb2.EmptyMessage())
            print ("[USER] Ho ricevuto il seguente id dalla richiesta di buy: ",str(response.id))
            
        else:
            numero_da_inviare=random.randint(1,100)
            response=stub.sell(service_pb2.SerialNumber(id=numero_da_inviare))
            print("[USER] Genero una richiesta di sell con il seguente numero: ",str(numero_da_inviare))
            if response.ack:
                print("[USER] Ho ricevuto l'ACK per la richiesta con il numero: ",str(numero_da_inviare))
            else :
                print("[USER] Qualcosa è andato storto")
            
            
        
        
if __name__=="__main__":
    try:
        port = sys.argv[1]
    except IOError:
        print("[USER] Riscrivi il porto")
    
    threads=[] 
    for i in range(10):
        th=mt.Thread(target=run_thread,args=(i,port))
        th.start()
        threads.append(th)
    
    for thread in threads:
        thread.join()
    
    