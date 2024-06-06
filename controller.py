from Model.model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def getProcView(self):
        self.view.printInfo(self.model.getProcInfos())

    def getProcInfo(self, pid):
        self.view.printProcInfo(self.model.getProcInfo(pid))

    def clearView(self):
        self.view.clear()

    def bye(self):
        self.view.bye()
