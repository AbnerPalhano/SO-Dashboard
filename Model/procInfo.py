from pathlib import Path
import asyncio
import re

# /proc/{pid}/net/dev é onde tem informações de uso de rede.
# /proc/stat info de uso global do processador
# /proc/{pid}/stat info de uso do processador no processo ((utime+stime)/starttime)
# /proc/meminfo info de uso global da ram


def findPids():
    pids = list()
    for folders in Path(f"/proc/").glob("[0-9]*"):
        pids.append(re.split(r"/proc/", folders.as_posix())[1])
    return pids


def procUser(Uid):
    for line in open(f"/etc/passwd", "r"):
        split = re.split(r":", line)
        if f"{Uid}" in split[2]:
            return split[0]


def statusRead(pid):
    try:
        for inf in open(f"/proc/{pid}/status", "r"):
            if "Name:" in inf:
                name = re.split(r"Name:\B", inf)[1].strip()
            elif "Uid:" in inf:
                uid = re.split(r"\s+", inf)[1]
            elif "State:" in inf:
                state = re.split(r"\s+", inf)[1]
        return name, uid, state
    except FileNotFoundError:
        return "", 0, ""
    except PermissionError:
        return "", 0, ""


def threadStatusRead(pid, tid):
    try:
        for inf in open(f"/proc/{pid}/task/{tid}/status", "r"):
            if "Name:" in inf:
                name = re.split(r"Name:\B", inf)[1].strip()
            elif "Uid:" in inf:
                uid = re.split(r"\s+", inf)[1]
            elif "State:" in inf:
                state = re.split(r"\s+", inf)[1]
        return name, uid, state
    except FileNotFoundError:
        return "", 0, ""
    except PermissionError:
        return "", 0, ""


def ioRead(pid):
    try:
        for inf in open(f"/proc/{pid}/io", "r"):
            if "read_bytes:" in inf:
                read = re.split(r"\s+", inf)[1]
            elif "write_bytes" in inf:
                write = re.split(r"\s+", inf)[1]
        return read, write
    except PermissionError:
        return 0, 0
    except FileNotFoundError:
        return 0, 0


def threadIoRead(pid, tid):
    try:
        for inf in open(f"/proc/{pid}/task/{tid}/io", "r"):
            if "read_bytes:" in inf:
                read = re.split(r"\s+", inf)[1]
            elif "write_bytes" in inf:
                write = re.split(r"\s+", inf)[1]
        return read, write
    except PermissionError:
        return 0, 0
    except FileNotFoundError:
        return 0, 0


async def getInfos(pid):
    infos = [0, "", "", "", 0, 0, list(), 0, 0]
    name, uid, state = statusRead(pid)
    read, write = ioRead(pid)
    infos[0], infos[1], infos[2], infos[3] = (
        pid,
        str(name),
        procUser(uid),
        cpuUsage(pid),
    )
    infos[4], infos[5], infos[6], infos[7] = (
        memoryUsage(pid),
        str(state),
        getThreads(pid),
        int(read),
    )
    infos[8] = int(write)
    return infos


def getThreadInfos(pid, tid):
    infos = [0, "", "", "", 0, 0, 0, 0]
    name, uid, state = threadStatusRead(pid, tid)
    read, write = threadIoRead(pid, tid)
    infos[0], infos[1], infos[2], infos[3] = (
        tid,
        str(name),
        procUser(uid),
        threadCpuUsage(pid, tid),
    )
    infos[4], infos[5], infos[6], infos[7] = (
        threadMemoryUsage(pid, tid),
        str(state),
        int(read),
        int(write),
    )
    return infos


async def getAllInfos():
    pids = findPids()
    tasks = [getInfos(pid) for pid in pids]
    pidList = await asyncio.gather(*tasks)
    return pidList


def getThreads(pid):
    try:
        threads = list()
        threadInfos = list()
        for folders in Path(f"/proc/{pid}/task/").glob("[0-9]*"):
            threads.append(
                re.split(r"/proc/" + re.escape(pid) + r"/task/", folders.as_posix())[1],
            )
        for thread in threads:
            threadInfos.append(getThreadInfos(pid, thread))
        return threadInfos
    except FileNotFoundError:
        return 0
    except PermissionError:
        return 0


def memoryUsage(pid):
    try:
        for inf in open(Path(f"/proc/{pid}/smaps_rollup"), "r"):
            if "Pss:" in inf and "SwapPss:" not in inf:
                mem = int(re.split(r"\s+", inf)[1])
        return mem
    except PermissionError:
        return 0
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0


def threadMemoryUsage(pid, tid):
    try:
        for inf in open(Path(f"/proc/{pid}/task/{tid}/smaps_rollup"), "r"):
            if "Pss:" in inf and "SwapPss:" not in inf:
                mem = int(re.split(r"\s+", inf)[1])
        return mem
    except PermissionError:
        return 0
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0


def cpuUsage(pid):
    try:
        stat = re.split(r"\s+", open(f"/proc/{pid}/stat", "r").read())
        uptime = float(re.split(r"\s+", open(f"/proc/uptime", "r").read())[0])
        utime = int(stat[13]) / 100
        stime = int(stat[14]) / 100
        starttime = float(stat[21]) / 100
        return ((utime + stime) * 100) / ((uptime - starttime))
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0
    except ZeroDivisionError:
        return 0


def threadCpuUsage(pid, tid):
    try:
        stat = re.split(r"\s+", open(f"/proc/{pid}/task/{tid}/stat", "r").read())
        uptime = float(re.split(r"\s+", open(f"/proc/uptime", "r").read())[0])
        utime = int(stat[13]) / 100
        stime = int(stat[14]) / 100
        starttime = float(stat[21]) / 100
        return ((utime + stime) * 100) / ((uptime - starttime))
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0
    except ZeroDivisionError:
        return 0


def main():
    return asyncio.run(getAllInfos())


if __name__ == "__main__":
    main()
