import stomp,sys,time
class MyListener(stomp.ConnectionListener):
    def __init__(self,parametro):
        self.parametro=parametro
    
    def on_message(self, frame):
        print("[BWPRINTER] Messaggio ricevuto: ",frame.body)
        if parametro in frame.body:
            print(f"[BWPRINTER] {parametro} è presente in {frame.body}")
            with open("bw.txt",'a') as file:
                file.write(frame.body+"\n")
        

if __name__=="__main__":
    try:
        parametro=sys.argv[1]
        if (parametro != "bw" and parametro !="gs"):
            exit(1)
    except IOError:
        print("Ritenta")
    
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.set_listener("",MyListener(parametro))
    conn.connect(wait=True)
    conn.subscribe(destination="/queue/bw",id=1,ack="auto")
    time.sleep(60)
    conn.disconnect()
    
    