from pathlib import Path
import time
import os
import re
import platform as pt

#/proc/{pid}/net/dev é onde tem informações de uso de rede.
#/proc/stat info de uso global do processador
#/proc/{pid}/stat info de uso do processador no processo ((utime+stime)/starttime)
#/proc/meminfo info de uso global da ram

def findPids():
    pids=list()
    for folders in Path(f'/proc/').glob('[0-9]*'):
        pids.append(re.split(r"/proc/",folders.as_posix())[1])
    return pids    

def procUser(Uid):
    for line in open(f"/etc/passwd","r"):
        split=re.split(r":",line)
        if(f"{Uid}" in split[2]):
            return split[0]
            
def statusRead(pid):
    try:
        for inf in open(f"/proc/{pid}/status","r"):
            if "Name:" in inf:
                name=re.split(r"Name:\B",inf)[1].strip()
            elif "Uid:" in inf:
                uid=re.split(r"\s+",inf)[1]
            elif "State:" in inf:
                state=re.split(r"\s+",inf)[1]     
        return name,uid,state
    except FileNotFoundError:
        return '',0,''
    except PermissionError:
        return '',0,''

def ioRead(pid):
    try:
        for inf in open(f'/proc/{pid}/io',"r"):
            if "read_bytes:" in inf:
                read=re.split(r"\s+",inf)[1]
            elif "write_bytes" in inf:
                write=re.split(r"\s+",inf)[1]
        return read,write
    except PermissionError:
        return 0,0
    except FileNotFoundError:
        return 0,0


def getInfos(pid):
    infos=[0,"","",'',0,0,0,0,0.0]
    name,uid,state = statusRead(pid)
    read,write=ioRead(pid)
    infos[0],infos[1],infos[2],infos[3]=pid,str(name),procUser(uid),cpuUsage(pid)
    infos[4],infos[5],infos[6],infos[7]=memoryUsage(pid),str(state),getThreads(pid),int(read)
    infos[8]=int(write)
    return infos
         
def getAllInfos():
    pids=findPids()
    pidList=list()
    for pid in pids:
        pidList.append(getInfos(pid))        
    return pidList
    
def getThreads(pid):
    try:
        threads=list()
        for folders in Path(f'/proc/{pid}/task/').glob('[0-9]*'):
            threads.append(re.split(r"/proc/"+re.escape(pid)+r"/task/",folders.as_posix())[1])
        return threads
    except FileNotFoundError:
        return 0
    except PermissionError:
        return 0
    
def memoryUsage(pid):
    try:
        for inf in open(Path(f'/proc/{pid}/smaps_rollup'),"r"):
            if "Pss:" in inf and "SwapPss:" not in inf:
                mem=int(re.split(r"\s+",inf)[1])
        return mem
    except PermissionError:
        return 0
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0
  
def cpuUsage(pid):
    try:
        stat=re.split(r"\s+",open(f'/proc/{pid}/stat',"r").read())
        uptime=float(re.split(r"\s+",open(f'/proc/uptime',"r").read())[0])
        utime=int(stat[13])/100
        stime=int(stat[14])/100
        starttime=float(stat[21])/100
        return (((utime+stime)*100)/((uptime-starttime)))
    except FileNotFoundError:
        return 0
    except ProcessLookupError:
        return 0
    except ZeroDivisionError:
        return 0  
    
def main():
    try:
        return getAllInfos()
    except KeyboardInterrupt:
        print(f'\nThe program has ended.\n')
    
if __name__ == '__main__':
    main()
