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

    def getDiskInfo(self, basepath):
        return asyncio.run(diskInfo.main(basepath))
