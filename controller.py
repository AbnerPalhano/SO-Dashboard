from Model.model import Model
from view import View
import os
import re


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def getProcView(self):
        self.view.printInfo(self.model.getProcInfos())

    def getProcInfo(self, pid):
        self.view.printProcInfo(self.model.getProcInfo(pid))

    def getFilesInfo(self, basepath):
        result = self.model.getFilesInfo(basepath)
        self.view.printStatx(result)
        return result[1]

    def getDiskInfo(self):
        self.view.printPartitionsInfo(self.model.getDiskInfo())

    def printMenu(self):
        self.view.printMenu()

    def printDiskInfoMenu(self):
        self.view.printDiskInfoMenu()

    def clearView(self):
        self.view.clear()

    def bye(self):
        self.view.bye()
