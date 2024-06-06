from Model.procInfo import *
import Model.procInfo as procInfo

class Model:
    def __init__(self) -> None:
        self.procList=list()
        self.globalInfo=list()
        
    def getProcInfos(self):
        self.procList=list()
        self.procList=procInfo.main()
        return self.procList
    
    def getProcInfo(self,pid):
        proc=asyncio.run(procInfo.getInfos(pid))
        return proc
    
