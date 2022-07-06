import os
import pathlib
import json

if os.name =='posix':
    import tkinter as tk
    from tkinter import ttk
    from tkinter import simpledialog
else:
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import simpledialog

PATH = str(pathlib.Path(__name__).parent.resolve())
FILEPATH = PATH + '/output/'

DRIVERPATH = PATH+'/chrome95/'

if os.name =='posix':
    DRIVERPATH += "linux/chromedriver"

