from Model.model import Model
from view import View
from controller import Controller

def main():
    model=Model()
    view=View()
    controller=Controller()
    opt='n'
    def printProcs():
        while(True):
            try:
                controller.getProcView()
            except KeyboardInterrupt:    
                opt=input("Do you want to exit? (y/n): ")
                if not 'n' in opt:
                    controller.clearView()
                    break

    def printProc(pid):
        while(True):
            try:
                controller.getProcInfo(pid)
            except KeyboardInterrupt:
                opt=input("Do you want to exit? (y/n): ")
                if not 'n' in opt:
                    controller.clearView()
                    break
    def run():
        while(True):
            controller.clearView()
            opt=input(f'start - print all processes\npid - print specific process info\nexit - exit\nEnter option: ')
            if opt=='start':
                printProcs()
            elif opt=='pid':
                controller.clearView()
                printProc(input('Enter PID: '))
            elif opt=='exit':
                controller.clearView()
                controller.bye()
                break
    
    run()
        
if __name__=="__main__":
    main()