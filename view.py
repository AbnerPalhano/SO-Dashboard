import os
import time
import sys


# import tkinter as tk
# from tkinter import ttk
class View:
    def printMenu(self):
        print("====================-----Dash board-----=====================")
        print("||command   -  description                                 ||")
        print(
            f"||s | start -  print all processes                         ||\n"
            + "||p | pid   -  print specific process info                 ||\n"
            + "||d | disk  -  print informations about disk and partitions||\n"
            + "||e | exit  -  exit the program                            ||"
        )
        print("=============================================================")
        print("Enter Command: ", end="")

    def printInfo(self, pidList):
        os.system("clear")

        list = sorted(pidList, key=lambda pidList: int(pidList[0]))
        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Threads":^5} | {"Read":^11} | {"Write":^11} |'
        )
        for inf in list:
            print(
                f"| {inf[0]:^6} | {inf[1]:^29} | {inf[2]:^15} |  {inf[3]:^6.2f}% | ",
                end="",
            )
            print(f"{inf[4]/1000:^8.2f}MB | {inf[5]:^7} | {len(inf[6]):^7} | ", end="")
            if inf[7] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                print(f"{inf[7]/1000000:^9.2f}MB | ", end="")
            if inf[8] == 0:
                print(f'{"N/A":^11} |')
            else:
                print(f"{inf[8]/1000000:^9.2f}MB |")
        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Threads":^5} | {"Read":^11} | {"Write":^11} |'
        )
        print(
            f"processos: {len(pidList)}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
        )
        print("Press CTRL+C to pause or return to menu.")
        print("It will return to the menu automatically if pressed twice.")
        time.sleep(1)

    def printProcInfo(self, proc):
        os.system("clear")
        print(
            f'| {"PID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Read":^11} | {"Write":^11} |'
        )
        print(
            f"| {proc[0]:^6} | {proc[1]:^29} | {proc[2]:^15} |  {proc[3]:^6.2f}% | ",
            end="",
        )
        print(f"{proc[4]/1000:^8.2f}MB | {proc[5]:^7} | ", end="")
        if proc[7] == 0:
            print(f'{"N/A":^11} | ', end="")
        else:
            print(f"{proc[7]/1000000:^9.2f}MB | ", end="")
        if proc[8] == 0:
            print(f'{"N/A":^11} |')
        else:
            print(f"{proc[8]/1000000:^9.2f}MB |")
        print(
            f'Threads:\n{"":^6}| {"TID":^6} | {"Name":^29} | {"User":^15} | {"CPU":^8} | {"Memory":^10} | {"State":^7} | {"Read":^11} | {"Write":^11} |'
        )
        for thread in proc[6]:

            print(
                f"{'':^6}| {thread[0]:^6} | {thread[1]:^29} | {thread[2]:^15} |  {thread[3]:^6.2f}% | ",
                end="",
            )
            print(f"{thread[4]/1000:^8.2f}MB | {thread[5]:^7} | ", end="")
            if thread[6] == 0:
                print(f'{"N/A":^11} | ', end="")
            else:
                print(f"{thread[6]/1000000:^9.2f}MB | ", end="")
            if thread[7] == 0:
                print(f'{"N/A":^11} |')
            else:
                print(f"{thread[7]/1000000:^9.2f}MB |")

        print(
            f"threads: {len(proc[6])}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
        )
        print("Press CTRL+C to pause or return to menu.")
        print("It will return to the menu automatically if pressed twice.")

        time.sleep(1)

    def printStatx(self, Statx):
        os.system("clear")
        for file, stat in Statx[0]:
            print(f"\n'{file.decode('utf-8')}'")
            print(f"Device major: {stat.stx_dev_major}")
            print(f"Device minor: {stat.stx_dev_minor}")
            print(f"Inode: {stat.stx_ino}")
            print(f"Mode: {oct(stat.stx_mode)}")
            print(f"Number of hard links: {stat.stx_nlink}")
            print(f"UID: {stat.stx_uid}")
            print(f"GID: {stat.stx_gid}")
            print(f"Size: {stat.stx_size} bytes")
            print(f"Block size: {stat.stx_blksize}")
            print(f"Number of blocks: {stat.stx_blocks}")
            print(f"Last access time: {stat.stx_atime.tv_sec}")
            print(f"Creation time: {stat.stx_btime.tv_sec}")
            print(f"Last modification time: {stat.stx_mtime.tv_sec}")
            print(f"Last status change time: {stat.stx_ctime.tv_sec}")
        print(f"\nContent of '{Statx[1].decode('utf-8')}':")
        for file, stat in Statx[0]:
            print(f"{os.path.basename(file.decode('utf-8'))} ", end="")
        print()

    def clear(self):
        os.system("clear")

    def bye(self):
        print("Bye! I hope this program made you happy :)")
