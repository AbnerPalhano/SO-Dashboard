import os
import time
import datetime
import Model.macros as macros
import Model.procInfo as procInfo


# import tkinter as tk
# from tkinter import ttk
class View:
    def printMenu(self):
        print("========================------SOdashboard------========================")
        print("|| commands -                  descriptions                          ||")
        print("||s | start -  print all processes                                   ||")
        print("||p | pid   -  print specific process info                           ||")
        print("||d | disk  -  print informations about disk and partitions          ||")
        print("||e | exit  -  exit the program                                      ||")
        print("||-------------------------------------------------------------------||")
        print("||info: Press ctrl+c to return to the menu from any of the options   ||")
        print("=======================================================================")
        print("Enter Command: ", end="")

    def printDiskInfoMenu(self):
        print("=======================-------Disk Info-------=========================")
        print("||    commands    -                   descriptions                   ||")
        print("|| f | files      - explore files and print files informations       ||")
        print("|| p | partitions - show a few informations about disk and partitions||")
        print("||-------------------------------------------------------------------||")
        print("||info: Press ctrl+c to return to the menu from files or partitions  ||")
        print("=======================================================================")

    def printPartitionsInfo(self, partitions):
        print("=======================-------Disk Info-------=========================")
        print(
            f"||     device name      |      device id      |        size          ||"
        )
        for part in partitions:
            id = f"{part[0]},{part[1]}"
            size = f"{float(part[2]):.2f}GB"
            print(f"||{part[3]:21} | {id:19} | {size:21}||")
        print("=======================================================================")

    def printInfo(self, pidList):
        os.system("clear")

        list = sorted(pidList, key=lambda pidList: int(pidList[0]))
        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^5} | {"Threads":^5} | {"Read":^11} | {"Write":^11} | {"opened files":^12} |'
        )
        for inf in list:
            print(
                f"| {inf[0]:^6} | {inf[1]:^29} | {inf[2]:^15} |  {inf[3]:^6.2f}% | ",
                end="",
            )
            memory = f"{inf[4]/1000:^.2f} MB"
            print(f"{memory:^10} | {inf[5]:^5} | {len(inf[6]):^7} | ", end="")
            if inf[7] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                read = f"{inf[7]/1000000:^.2f} MB"
                print(f"{read:^11} | ", end="")
            if inf[8] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                write = f"{inf[8]/1000000:^.2f} MB"
                print(f"{write:^11} | ", end="")
            print(f"{inf[9]:^12} |")

        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^5} | {"Threads":^5} | {"Read":^11} | {"Write":^11} | {"opened files":^12} |'
        )
        print(
            f"processos: {len(pidList)}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
        )
        print("Press ctrl+c to pause or return to menu.")
        print("It will return to the menu automatically if pressed twice.")
        time.sleep(1)

    def printProcInfo(self, proc):
        os.system("clear")
        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Read":^11} | {"Write":^11} | {"opened files":^12} |'
        )
        print(
            f"| {proc[0]:^6} | {proc[1]:^29} | {proc[2]:^15} |  {proc[3]:^6.2f}% | ",
            end="",
        )
        memory = f"{proc[4]/1000:^.2f} MB"
        print(f"{memory:^10} | {proc[5]:^7} | ", end="")
        if proc[7] == 0:
            print(f'{"N/A":^11} | ', end="")
        else:
            read = f"{proc[7]/1000000:^.2f} MB"
            print(f"{read:^11} | ", end="")
        if proc[8] == 0:
            print(f'{"N/A":^11} | ', end="")
        else:
            write = f"{proc[8]/1000000:^.2f} MB"
            print(f"{write:^11} | ", end="")
        print(f"{proc[9]:^12} |")
        print(
            f'{"":^6}| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Read":^11} | {"Write":^11} | {"opened files":^12} |'
        )

        for thread in proc[6]:

            print(
                f"{'':^6}| {thread[0]:^6} | {thread[1]:^29} | {thread[2]:^15} |  {thread[3]:^6.2f}% | ",
                end="",
            )
            memory = f"{thread[4]/1000:^.2f} MB"
            print(f"{memory:^10} | {thread[5]:^7} | ", end="")
            if thread[6] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                read = f"{thread[6]/1000000:^.2f} MB"
                print(f"{read:^11} | ", end="")
            if thread[7] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                write = f"{thread[7]/1000000:^.2f} MB"
                print(f"{write:^11} | ", end="")
            print(f"{thread[8]:^12} |")

        print(
            f"threads: {len(proc[6])}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
        )
        print("Press ctrl+c to pause or return to menu.")
        print("It will return to the menu automatically if pressed twice.")

        time.sleep(1)

    def printStatx(self, Statx):
        os.system("clear")
        for file, stat in Statx[0]:
            print(f"\n'{file.decode('utf-8')}'")
            print(f"type: {stat[1]}  permissions: {stat[2]}")
            print(
                f"Size: {stat[0].stx_size} bytes  Blocks: {stat[0].stx_blocks}  Block size: {stat[0].stx_blksize}"
            )

            print(
                f"Device: {stat[0].stx_dev_major},{stat[0].stx_dev_minor}  Inode: {stat[0].stx_ino}  Links: {stat[0].stx_nlink}"
            )
            print(
                f"Access:({oct(stat[0].stx_mode)[-4:]}/{stat[2]})  UID: ({stat[0].stx_uid}/ {procInfo.procUser(stat[0].stx_uid)})  GID: ({stat[0].stx_gid}/ {procInfo.procGroup(stat[0].stx_gid)})"
            )
            print(
                f"Last access time: {datetime.datetime.fromtimestamp(stat[0].stx_atime.tv_sec)}"
            )
            print(
                f"Creation time: {datetime.datetime.fromtimestamp(int(stat[0].stx_btime.tv_sec))}"
            )
            print(
                f"Last modification time: {datetime.datetime.fromtimestamp(stat[0].stx_mtime.tv_sec)}"
            )
            print(
                f"Last status change time: {datetime.datetime.fromtimestamp(stat[0].stx_ctime.tv_sec)}"
            )
        print(f"\nContent of '{Statx[1].decode('utf-8')}':")
        for file, stat in Statx[0]:
            print(f"{os.path.basename(file.decode('utf-8'))} ", end="")
        print()

    def clear(self):
        os.system("clear")

    def bye(self):
        print("Bye! I hope you liked this program :)")
