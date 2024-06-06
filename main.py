from Model.model import Model
from view import View
from controller import Controller


def main():
    model = Model()
    view = View()
    controller = Controller()
    opt = "n"

    def printProcs():
        while True:
            try:
                controller.getProcView()
            except KeyboardInterrupt:
                try:
                    if not "n" in input("\nDo you want to continue? [y/n]: "):
                        continue
                except KeyboardInterrupt:
                    controller.clearView()
                    break
                controller.clearView()
                break

    def printProc(pid):
        while True:
            try:
                controller.getProcInfo(pid)
            except KeyboardInterrupt:
                try:
                    if not "n" in input("\nDo you want to continue? [y/n]: "):
                        continue
                except KeyboardInterrupt:
                    controller.clearView()
                    break
                controller.clearView()
                break

    def run():
        while True:
            controller.clearView()
            try:
                opt = input(
                    f"start - print all processes\n"
                    + "pid - print specific process info\n"
                    + "disk - print informations about disk and partitions (wip)\n"
                    + "exit - exit the program\n"
                    + "Enter option: "
                )
                if opt == "start":
                    printProcs()
                elif opt == "pid":
                    controller.clearView()
                    try:
                        printProc(input("Enter PID: "))
                    except KeyboardInterrupt:
                        continue
                elif opt.isnumeric():
                    printProc(opt)
                elif opt == "disk":
                    controller.clearView()
                    controller.getDiskInfo()
                elif opt == "exit":
                    controller.clearView()
                    controller.bye()
                    break
                else:
                    controller.clearView()
                    try:
                        input(
                            f"'{opt}' is not a valid option, press any key to continue."
                        )
                    except KeyboardInterrupt:
                        continue
            except KeyboardInterrupt:
                controller.clearView()
                controller.bye()
                break
            except BaseException as e:
                try:
                    input(f"Error: {e}, press any key to continue.")
                except KeyboardInterrupt:
                    continue
                continue

    run()


if __name__ == "__main__":
    main()
