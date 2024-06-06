from Model.procInfo import *
from Model.diskInfo import *
import Model.procInfo as procInfo
import Model.diskInfo as diskInfo


class Model:
    def __init__(self) -> None:
        self.procList = list()
        self.globalInfo = list()

    def getProcInfos(self):
        self.procList = list()
        self.procList = procInfo.main()
        return self.procList

    def getProcInfo(self, pid):
        return asyncio.run(procInfo.getInfos(pid))

    def getDiskInfo(self):
        return asyncio.run(diskInfo.main())
