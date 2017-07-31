"""GUI class definition for main window
"""

import configparser
import pathlib
from tkinter import BOTH, Menu, PhotoImage, StringVar, Text, W, X
from tkinter.ttk import Button, Frame, Menubutton, Style

from gui.conf_win import ConfWin


class AppWin(Frame):

    def __init__(self, master=None, **kw):

        # root Tk
        self.master = master

        self.master.title(kw.get('app_title', 'Sync-Dev'))

        # default dimensions for main window
        w = kw.get('width', 330)
        h = kw.get('width', 250)

        # user screen(monitor) dimensions
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        # fixing minimal window size
        self.master.minsize(330, 250)

        # sizeing and centralizing main window

        self.master.geometry(
            '%dx%d+%d+%d' % (
                w,
                h,
                (ws / 2) - (w / 2),
                (hs / 2) - (h / 2)
            )
        )

        self.build_menu()

        # user style define
        frame_style = kw.get('style', None)

        # changing main window background to white

        if frame_style is None:

            # creating default Frame style
            frame_style = Style()

            frame_style.configure(
                'SyncDev.TFrame',
                foreground='black',
                background='white'
            )

            kw.update({
                'style': 'SyncDev.TFrame'
            })

        # instancing Frame object
        Frame.__init__(self, master, **kw)

        # load icons for main routines
        self.icon_mob_pc = PhotoImage(file=pathlib.Path('./rsc/img/mobile_to_pc.png'))
        self.icon_pc_mob = PhotoImage(file=pathlib.Path('./rsc/img/pc_to_mobile.png'))

        # conf ini variables to get value from form window
        self.ents = []
        self.adb_path = StringVar()
        self.syncdev_json_path = StringVar()
        self.db_host = StringVar()
        self.db_user = StringVar()
        self.db_port = StringVar()

        # init Configuration Parser
        self.prefs_ini = configparser.ConfigParser()

        # read prefs.ini configuration
        self.prefs_ini.read('./rsc/cnf/prefs.ini')

        # user defined gui
        self.sync_buttons()

        self.add_log_entry()

    def build_menu(self):

        # Main Menu
        menubtn = Menubutton(self.master, text='Preferências')

        # Menu creating
        pref_opts = Menu(menubtn, tearoff=False)

        # linking each other
        menubtn.config(menu=pref_opts)

        # adding options
        pref_opts.add_command(label='Configurações', command=self.call_conf_win)

        pref_opts.add_command(label='Exit', command=self.exit_app_win)

        # align left
        menubtn.pack(anchor=W)

    def call_conf_win(self):

        ConfWin(self)

    def sync_buttons(self):

        style = Style()

        style.configure(
            'MobPc.TButton',
            image=self.icon_mob_pc,
            font='size 14'
        )

        style.configure(
            'PcMob.TButton',
            image=self.icon_pc_mob,
            font='size 14'
        )

        btn_read = Button(
            self,
            text="Móvel para Desktop",
            style='MobPc.TButton',
            compound='left'
        )

        self.btn_write = Button(
            self,
            text="Desktop para Móvel",
            style='PcMob.TButton',
            compound='left'
        )

        btn_read.pack(fill=X)
        self.btn_write.pack(fill=X)

    def add_log_entry(self):

        self.ety_log = Text(self)
        self.ety_log.pack(expand=True,fill=BOTH)

    def exit_app_win(self):

        self.master.quit()
