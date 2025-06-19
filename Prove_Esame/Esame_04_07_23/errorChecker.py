import stomp,time
class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print("[ERRORCHECKER] Ricevuto messaggio:",frame.body)
        with open("error.txt",'a') as file:
            file.write(frame.body+"\n")
            
    
if __name__=="__main__":
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.set_listener("",MyListener())
    conn.connect(wait=True)
    conn.subscribe(destination="/queue/error",id=1,ack="auto")
    while True:
        time.sleep(60)
    conn.disconnect()