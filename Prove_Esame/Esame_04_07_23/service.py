import sys,random
from clientProxy import ClientProxy
if __name__=="__main__":
    try:
        port=sys.argv[1]
    except IOError:
        print("[SERVICE] Ritenta a scrivere il porto")
    
    list=["success","checking","fatal","exception"]
    proxy=ClientProxy(port)
    for i in range(10):
        tipo=random.randint(0,2)
        print(f"[SERVICE] Sto creando la richiesta nr {str(i)}")
        if tipo==2:
            proxy.log(list[random.randint(2,3)],tipo)
        else:
            proxy.log(list[random.randint(0,1)],tipo)
        
            
        
    