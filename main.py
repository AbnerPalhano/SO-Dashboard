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
                    f"s | start - print all processes\n"
                    + "p | pid - print specific process info\n"
                    + "d | disk - print informations about disk and partitions (wip)\n"
                    + "e | exit - exit the program\n"
                    + "Enter option: "
                )
                if opt == "start" or opt == "s":
                    printProcs()
                elif opt == "pid" or opt == "p":
                    controller.clearView()
                    try:
                        printProc(input("Enter PID: "))
                    except KeyboardInterrupt:
                        continue
                elif opt.isnumeric():
                    printProc(opt)
                elif opt == "disk" or opt == "d":
                    controller.clearView()
                    while True:
                        try:
                            controller.getDiskInfo()
                        except KeyboardInterrupt:
                            break

                elif opt == "exit" or opt == "e":
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
