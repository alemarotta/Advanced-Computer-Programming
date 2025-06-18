from proxy import Proxy
import sys,random
if __name__=="__main__":
    try:
       PORT=sys.argv[1]
    except IOError:
        print("Ritenta") 
    
    p = Proxy(PORT)
    for i in range(10):
        colori=["bw","gs","color"]
        estensioni=["doc","txt"]
        num=random.randint(0,100)
        print("[CLIENT] Ho generato la richiesta numero ",str(i))
        p.print(f"/user/file_{num}.{estensioni[random.randint(0,1)]}",colori[random.randint(0,2)])