import requests
import grpc,service_pb2,service_pb2_grpc
from threading import Lock,Condition
from concurrent import futures
server_address="http://127.0.0.1:5001"
class ProductManager(service_pb2_grpc.ProductMaanagerServicer):
    def __init__(self):
        self.queue=[]
        self.size=5
        
        self.lock_coda=Lock()
        self.cv_consuma=Condition(self.lock_coda)
        self.cv_produci=Condition(self.lock_coda)
    
    def sell(self, request, context):
        with self.cv_produci:
            while(self.isFull()):
                self.cv_produci.wait()
            print("[PRODUCT MANAGER] Ho ricevuto il seguente id: ",str(request.id))
            self.queue.append(request.id)
            resource_location=server_address+"/update_history"
            req_dict={
                "operation":"sell",
                "serial_number":request.id
            }
            
            response=requests.post(resource_location,json=req_dict)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f"[PRODUCT MANAGER] Error: Received {response.status_code} - {response.text}")
                return service_pb2.Ack(ack=False)
            else:
                return service_pb2.Ack(ack=True)
            finally:
                self.cv_consuma.notify()
        
        
    def buy(self, request, context):
        with self.cv_consuma:
            while(self.isEmpty()):
                self.cv_consuma.wait()
            id_elemento=self.queue.pop()
            resource_location=server_address+"/update_history"
            req_dict={
                "operation":"buy",
                "serial_number":id_elemento
            }
            
            response=requests.post(resource_location,json=req_dict)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f"[PRODUCT MANAGER] Error: Received {response.status_code} - {response.text}")
            else:
                return service_pb2.ExtractedProduct(id=id_elemento)
            finally:
                self.cv_produci.notify()
            
    
    def isEmpty(self):
        return len(self.queue)==0
    
    def isFull(self):
        return len(self.queue)==self.size
    
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ProductMaanagerServicer_to_server(ProductManager(),server)
    
    port=server.add_insecure_port("0.0.0.0:0")
    print("[PRODUCT MANAGER] Sono in ascolto su porto: ",str(port))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
	serve()