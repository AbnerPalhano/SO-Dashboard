from Model.model import Model
from view import View
from controller import Controller

model=Model()
view=View()
controller=Controller()
while(True):
    try:
        controller.updateView()
    except KeyboardInterrupt:
        print(f'programa finalizado')
        break