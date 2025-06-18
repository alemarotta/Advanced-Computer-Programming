import stomp,requests,time
server_address="http://localhost:5001"
class MyListener(stomp.ConnectionListener):
    def __init__(self,conn):
        self.conn=conn
    def on_message(self, frame):
        print("[BOOKINGMANAGER] Ho ricevuto la seguente richiesta",frame.body)
        richiesta=frame.body.split("-")[0]
        if richiesta=="CREATE":
            dict_Create={
                "client":frame.body.split("-")[1],
                "hotel":frame.body.split("-")[2],
                "operator":frame.body.split("-")[3],
                "nights":int(frame.body.split("-")[4]),
                "people":int(frame.body.split("-")[5]),
                "cost":int(frame.body.split("-")[6])
            }
            try:
                resource_location=server_address+"/create_booking"
                response = requests.put(url=resource_location, json=dict_Create)
                response.raise_for_status()
                print(f"[BOOKING MANAGER] Sent CREATE request correctly to database. status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print("[BOOKING MANAGER] Error while sending the CREATE request")
            else:
                conn.send(body="ACK", destination="/topic/response")
            
        elif richiesta=="UPDATE":
            dict_Update={
                "operator":frame.body.split("-")[1],
                "discount":int(frame.body.split("-")[2]),
                "nights":int(frame.body.split("-")[3])
            }
            try:
                resource_location=server_address+"/update_booking"
                response=requests.post(url=resource_location,json=dict_Update)
                response.raise_for_status()
                print(f"[BOOKING MANAGER] Sent CREATE request correctly to database. status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print("[BOOKING MANAGER] Error while sending the CREATE request")
            else:
                conn.send(body="ACK", destination="/topic/response")

if __name__=="__main__":
    conn=stomp.Connection([("127.0.0.1","61613")])
    conn.set_listener("",MyListener(conn))
    conn.connect(wait=True)
    conn.subscribe("/topic/request",id=1,ack="auto")
    while True:
        time.sleep(60)
    conn.disconnect()