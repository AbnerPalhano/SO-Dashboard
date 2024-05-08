import os
import time
import tkinter as tk
from tkinter import ttk
class View:   
    def printInfo(self,pidList):
        table=tk.Tk()
        label=tk.Label(table,text="procs",font=('sans serif',30)).grid(row=0,columnspan=3)
        cols=('PID','Name','User','State','CPU Usage','Memory Usage','Num of Threads','Disk Read','Disk Write')
        listBox=ttk.Treeview(table,columns=cols,show='headings')
        
        for col in cols:
            listBox.heading(col,text=col)
        listBox.grid(row=1,column=0,columnspan=1)
        
        for pid in pidList:
            listBox.insert("","end",values=pid)
        table.mainloop()
        
        '''
        os.system('clear')
        list=sorted(pidList,key=lambda pidList:pidList[8])
        for inf in list:
            print(f'{inf[0]} | {inf[1]} | {inf[2]} | {inf[3]} | ',end='')
            if inf[4]==0:
                print(f'N/A | ',end='')
            else:
                print(f'{inf[4]/1000000:.2f}MB | ',end='')
            if inf[5]==0:
                print(f'N/A | ',end='')
            else:
                print(f'{inf[5]/1000000:.2f}MB | ',end='')
            print(f'{len(inf[6])} | {inf[7]/1000:.2f}MB | {inf[8]:.2f}%')
        print(f'processos: {len(pidList)}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec:2d}')
        time.sleep(2)
        '''
 