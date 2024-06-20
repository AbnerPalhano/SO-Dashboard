from Model.procInfo import *
from Model.diskInfo import *
import Model.procInfo as procInfo
import Model.diskInfo as diskInfo


class Model:
    def __init__(self) -> None:
        print("Model created")

    def getProcInfos(self):
        return procInfo.main()

    def getProcInfo(self, pid):
        return asyncio.run(procInfo.getInfos(pid))

    def getFilesInfo(self, basepath):
        return asyncio.run(diskInfo.getStatx(basepath))

    def getDiskInfo(self):
        return diskInfo.readpartitions()
