"""entry point for Pysync-dev module
"""

# TODO
# ###
#  Validating if adb found a device
# Transfer sync JSON to Mobile
# ###
# Sync Entities Json to Desktop
# Read Mobile JSON
# Connect to PG
# Persist Data
####

from tkinter import Tk, BOTH

from gui.app_win import AppWin

from ctrl.sync_to_mobile import sync_para_movel

if __name__ == '__main__':

    root = Tk()

    root.iconbitmap('./rsc/img/pysyncsync.ico')

    sync_sync = AppWin(root)

    sync_sync.pack(fill=BOTH, expand=1)

    sync_sync.btn_write.configure(command= lambda: sync_para_movel(sync_sync))

    root.mainloop()
