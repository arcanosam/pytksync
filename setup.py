""" Packaging and distribution using cx-freeze on Windows Plataform only
"""
import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:\\pysyncdev\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\pysyncdev\\tcl\\tk8.6'

build_exe_options = {
    'include_msvcr': True,   #skip error msvcr100.dll missing
    'includes': [
        'gui.app_win',
        'gui.conf_win'
    ],
    'include_files': [
        'C:\\pysyncdev\\DLLs\\tcl86t.dll', 
        'C:\\pysyncdev\\DLLs\\tk86t.dll'
    ]
}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name='pysyncdev',
    version='0.1',
    description='pysyncdev',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py', base=base)]
)
