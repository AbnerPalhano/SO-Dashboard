from Model.model import Model
from view import View

class Controller:
    def __init__(self):
        self.model=Model()
        self.view=View()
        
    def getAll(self):
        self.model.getProcInfos()
        self.updateView()
    def getProcView(self):
        procs=self.model.getProcInfos()
        self.view.printInfo(procs)
    def getProcInfo(self,pid):
        proc=self.model.getProcInfo(pid)
        self.view.printProcInfo(proc)
    
    def clearView(self):
        self.view.clear()
    def bye(self):
        self.view.bye()