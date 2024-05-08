from Model.model import Model
from view import View

class Controller:
    def __init__(self):
        self.model=Model()
        self.view=View()
        
    def getAll(self):
        self.model.getProcInfos()
        self.updateView()
    def updateView(self):
        procs=self.model.getProcInfos()
        self.view.printInfo(procs)