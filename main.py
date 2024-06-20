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
                    controller.printDiskInfoMenu()
                    exit = False
                    stay = True
                    while True and not exit and stay:
                        try:
                            controller.clearView()
                            controller.printDiskInfoMenu()

                            optDiskInfo = input("Enter Command: ")
                        except KeyboardInterrupt:
                            exit = True
                            break
                        if (
                            optDiskInfo == "partitions"
                            or optDiskInfo == "p"
                            or optDiskInfo == "P"
                        ):
                            controller.clearView()
                            controller.getDiskInfo()
                            try:
                                input(
                                    "press any key to continue, or ctrl+c to return to the menu"
                                )
                            except KeyboardInterrupt:
                                exit = True
                                break
                        elif (
                            optDiskInfo == "files"
                            or optDiskInfo == "f"
                            or optDiskInfo == "F"
                        ):
                            stay = True
                            while True:
                                try:
                                    controller.clearView()
                                    searchPath = bytes(
                                        input(
                                            "enter path (leave empty to start at the project folder or enter the full path, starting from the root folder '/'): "
                                        ).encode("utf-8")
                                    )
                                except KeyboardInterrupt:
                                    stay = False
                                    exit = True
                                    break
                                if not searchPath:
                                    searchPath = bytes(os.getcwd().encode("utf-8"))
                                    break
                                elif re.search("[..]", str(searchPath)):
                                    searchPath = bytes(
                                        os.path.dirname(os.getcwd().encode("utf-8"))
                                    )
                                elif not str(searchPath).startswith("/", 0, 0):
                                    searchPath = (
                                        bytes(str("/").encode("utf-8")) + searchPath
                                    )

                                if not os.path.exists(searchPath):
                                    input(
                                        f"'{searchPath.decode('utf-8')}' don't exist, press any key to continue..."
                                    )
                                    controller.clearView()
                                    continue
                                break
                            while True and stay:
                                try:
                                    path = controller.getFilesInfo(searchPath)
                                    while True and stay:
                                        try:
                                            searchPath = os.path.join(
                                                path,
                                                bytes(
                                                    input(
                                                        f"Enter new path (Enter '..' to go to parent folder): "
                                                    ).encode("utf-8")
                                                ),
                                            )
                                        except KeyboardInterrupt:
                                            stay = False
                                            break
                                        if os.path.isfile(searchPath):
                                            print(
                                                f"'{searchPath.decode('utf-8')}' is a file, not a directory!"
                                            )
                                            continue
                                        if not os.path.exists(searchPath):
                                            print(
                                                f"'{searchPath.decode('utf-8')}' don't exist!"
                                            )
                                            continue
                                        break

                                except KeyboardInterrupt:
                                    stay = False
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
