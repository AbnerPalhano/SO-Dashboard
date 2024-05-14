import os
import time
#import tkinter as tk
#from tkinter import ttk
class View:   
    def printInfo(self,pidList):
        '''
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
        list=sorted(pidList,key=lambda pidList:pidList[0])
        for inf in list:
            print(f'{inf[0]} | {inf[1]} | {inf[2]} |  {inf[3]:.2f}% | ',end='')
            print(f'{inf[4]/1000:.2f}MB | {inf[5]} | {len(inf[6])} | ',end='')
            if inf[7]==0:
                print(f'N/A | ',end='')
            else:
                print(f'{inf[7]/1000000:.2f}MB | ',end='')
            if inf[8]==0:
                print(f'N/A')
            else:
                print(f'{inf[8]/1000000:.2f}MB')
        print(f'processos: {len(pidList)}\nhora: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec:2d}')
        time.sleep(2)
        
 