import os
import time
import sys


# import tkinter as tk
# from tkinter import ttk
class View:
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
        sys.stdout.flush()
        time.sleep(1)

    def clear(self):
        os.system("clear")

    def bye(self):
        print("Bye!")
