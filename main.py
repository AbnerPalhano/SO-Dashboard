from Model.model import Model
from view import View
from controller import Controller
import os
import re


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
            controller.printMenu()
            try:
                opt = input()
                if opt == "start" or opt == "s" or opt == "S":
                    printProcs()
                elif opt == "pid" or opt == "p" or opt == "P":
                    controller.clearView()
                    try:
                        printProc(input("Enter PID: "))
                    except KeyboardInterrupt:
                        continue
                elif opt.isnumeric():
                    printProc(opt)
                elif opt == "disk" or opt == "d" or opt == "D":
                    controller.clearView()
                    while True:
                        searchPath = bytes(
                            input(
                                "enter path (leave empty to start at the project folder):"
                            ).encode("utf-8")
                        )
                        if not searchPath:
                            searchPath = bytes(os.getcwd().encode("utf-8"))
                            break
                        elif re.search("[..]", str(searchPath)):
                            searchPath = bytes(
                                os.path.dirname(os.getcwd().encode("utf-8"))
                            )
                        elif not re.search("^[/]", str(searchPath)):
                            searchPath = bytes(str("/").encode("utf-8")) + searchPath

                        if not os.path.exists(searchPath):
                            input(
                                f"'{searchPath.decode('utf-8')}' don't exist, press any key to continue..."
                            )
                            controller.clearView()
                            continue
                        break
                    while True:
                        try:
                            path = controller.getDiskInfo(searchPath)
                            if not os.path.isdir(path):
                                print(f"{searchPath} is a file, not a directory!")
                                continue
                            while True:
                                searchPath = os.path.join(
                                    path,
                                    bytes(input(f"enter new path:").encode("utf-8")),
                                )
                                if not os.path.exists(searchPath):
                                    print(
                                        f"'{searchPath.decode('utf-8')}' don't exist",
                                        end=", ",
                                    )
                                    continue
                                break

                        except KeyboardInterrupt:
                            break

                elif opt == "exit" or opt == "e" or opt == "E":
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
