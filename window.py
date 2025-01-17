# TODO: turn into run.bat and build.bat (or .sh for linux?)
# python3.12 window.py
# pyinstaller --onefile window.py
# pyinstaller window.spec
import PySimpleGUI as gui
import logging
import samase
import os

LOGFILE = "sezam.log"

def assert_path(path: str, message: str = "Attempted to perform an operation without a directory selected!") -> bool:
    if path == "" or path is None:
        print(message)
        return False
    return True

class Window():
    def __init__(self):
        # TODO: supply intelligent defaults
        self.local_samase = ""
        self.unpack_samase = ""

        layout = [[gui.Button("Select build directory"), gui.Text("Please select a path", key="curPath"), gui.Push(), gui.Checkbox("Run in x64", key="x64")],
                [gui.Push(), gui.Button("Launch"), gui.Button("Build From"), gui.Push()],
                [gui.Push()],
                [gui.Button("Select .exe to Unpack"), gui.Text("No exe selected", key="curExe")],
                [gui.Push(), gui.Button("Unpack from"), gui.Push()]
        ]
        self.window = gui.Window("Sezam", layout, resizable=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == gui.WIN_CLOSED:
                break
            if event == "Select build directory":
                directory = gui.popup_get_folder('Select path', initial_folder=os.getcwd())
                if not assert_path(directory, "Nothing selected"):
                    continue
                clean_dir = directory[(directory.rfind("/")+1):] # TODO: use appropriate function from os.path
                self.window["curPath"].update(value=clean_dir)
                self.local_samase = directory
            if event == "Select .exe to Unpack":
                directory = gui.popup_get_file('Select path', initial_folder=os.getcwd(), file_types=(("Executable files", "*.exe"),))
                if not assert_path(directory, "Nothing selected"):
                    continue
                clean_dir = directory[(directory.rfind("/")+1):]
                self.window["curExe"].update(value=clean_dir)
                self.unpack_samase = directory
            if event == "Launch":
                if not assert_path(self.local_samase):
                    continue
                samase.run(self.local_samase, values["x64"])
            if event == "Build From":
                if not assert_path(self.local_samase):
                    continue
                samase.build(self.local_samase, values["x64"])
            if event == "Unpack from":
                if not assert_path(self.unpack_samase):
                    continue
                # on assumption that the user must select .exe file in the popup
                assert self.unpack_samase.endswith(".exe"), f"Expected executable to unpack, instead got {self.local_samase}"
                samase.build(self.unpack_samase, values["x64"])

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.FileHandler(LOGFILE, mode = "w")

    window = Window()
    window.run()
    