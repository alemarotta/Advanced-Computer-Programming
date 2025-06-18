import stomp,sys,time
class MyListener(stomp.ConnectionListener):
    def __init__(self,parametro):
        self.parametro=parametro
    
    def on_message(self, frame):
        print("[COLORPRINTER] Messaggio ricevuto: ",frame.body)
        if parametro in frame.body:
            print(f"[COLORPRINTER] {parametro} è presente in {frame.body}")
            with open("color.txt",'a') as file:
                file.write(frame.body+"\n")
        

if __name__=="__main__":
    try:
        parametro=sys.argv[1]
        if (parametro != "doc" and parametro!="txt"):
            exit(1)
    except IOError:
        print("Ritenta")
    
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.set_listener("",MyListener(parametro))
    conn.connect(wait=True)
    conn.subscribe(destination="/queue/color",id=1,ack="auto")
    while True:
        time.sleep(60)
    conn.disconnect()
    
    