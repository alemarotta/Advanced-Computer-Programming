from abc import ABC,abstractmethod

class Interface (ABC):
    def deposita(self,articolo,id):
        pass
    def preleva(self,articolo):
        pass