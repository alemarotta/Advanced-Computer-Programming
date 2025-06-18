from Skeleton import Skeleton
from multiprocessing import Queue
class SkeletonImpl(Skeleton):
    def __init__(self, host, port,queue=Queue(5)):
        super().__init__(host, port)
        self.queue=queue
    
    def print(self, pathFile, tipo):
        messaggio=pathFile+"-"+tipo
        self.queue.put(messaggio)
        print("[SKELETONIMPL] Ho inserito il messaggio nella coda")
    
    def consuma(self):
        message=self.queue.get()
        print("[SKELETONIMPL] Ho prelevato il messaggio dalla coda")
        return message