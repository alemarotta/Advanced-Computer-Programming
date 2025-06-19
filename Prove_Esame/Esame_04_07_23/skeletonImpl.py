from skeleton import Skeleton
import multiprocessing as mp
class SkeletonImpl(Skeleton):
    def __init__(self):
        super().__init__()
        self.queue=mp.Queue(5)
        
        
    def log(self, messaggio, tipo):
        message_to_enqueue=messaggio+"-"+str(tipo)
        self.queue.put(message_to_enqueue)
        print("[SKELETONIMPL] Ho inserito in coda")
    
    def consuma(self):
        message_to_return=self.queue.get()
        print("[SKELETONIMPL] Ho prelevato dalla coda")
        return message_to_return
