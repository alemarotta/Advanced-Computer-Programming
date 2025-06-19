from interface import Interface
from threading import Lock,Condition
class SkeletonImpl(Interface):
    def __init__(self):
        self.queue_laptop=[]
        self.queue_smartphone=[]
        self.lock_laptop=Lock()
        self.lock_smartphone=Lock()
        self.cv_consuma_laptop=Condition(self.lock_laptop)
        self.cv_produci_laptop=Condition(self.lock_laptop)
        self.cv_consuma_smartphone=Condition(self.lock_smartphone)
        self.cv_produci_smartphone=Condition(self.lock_smartphone)
        self.queue_size=5
        
        
    def deposita(self, articolo, id):
        if articolo=="laptop":
            with self.cv_produci_laptop:
                while(self.isFull(self.queue_laptop)):
                    self.cv_produci_laptop.wait()
                
                self.queue_laptop.append(id)
                self.cv_consuma_laptop.notify()
                print("[SKELETONIMPL] Ho depositato nella coda laptop")
                with open("laptop.txt",'a') as file:
                    file.write(str(id)+"\n")
        else:
            with self.cv_produci_smartphone:
                while(self.isFull(self.queue_smartphone)):
                    self.cv_produci_smartphone.wait()
                
                self.queue_smartphone.append(id)
                self.cv_consuma_smartphone.notify()
                print("[SKELETONIMPL] Ho depositato nella coda smartphone")
                with open("smartphone.txt",'a') as file:
                    file.write(str(id)+"\n")
                
    def preleva(self, articolo):
        if articolo=="laptop":
            with self.cv_consuma_laptop:
                while(self.isEmpty(self.queue_laptop)):
                    self.cv_consuma_laptop.wait()
                
                print("[SKELETONIMPL] Ho prelevato dalla coda laptop")
                self.queue_laptop.pop()
                self.cv_produci_laptop.notify()
        else:
            with self.cv_consuma_smartphone:
                while(self.isEmpty(self.queue_smartphone)):
                    self.cv_consuma_smartphone.wait()
                print("[SKELETONIMPL] Ho prelevato dalla coda smartphone")
                self.queue_smartphone.pop()
                self.cv_produci_smartphone.notify()
    
    def isEmpty(self,queue):
        return len(queue)==0
    
    def isFull(self,queue):
        return len(queue)==self.queue_size
    