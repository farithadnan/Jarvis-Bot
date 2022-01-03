import os
import subprocess as sp

paths = {
    'discord': "C:\\Users\\Farith Adnan\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'vscode': "C:\\Users\\Farith Adnan\\AppData\\Local\\Programs\\Microsoft VS Code"
}

# Functions to open app based on the given path
def open_vscode():
    os.startfile(paths['vscode'])


def open_discord():
    os.startfile(paths['discord'])

# Functions to prompt cmd
def open_cmd():
    os.system('start cmd')

# Functions to open camera on system
def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])