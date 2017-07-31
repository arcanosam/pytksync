""" Configuration INI window definitions
"""

import configparser

import glob

import os

from tkinter import BOTH, END, EXTENDED, filedialog, Listbox, LEFT, RIDGE, \
                    NW, RIGHT, Scrollbar, TOP, Toplevel, VERTICAL, X, Y

from tkinter.messagebox import  askyesno, showerror, showinfo

from tkinter.ttk import Button, Entry, Frame, Label

from ctrl.core import verif_ha_entidade_selecionada


class ConfWin(Toplevel):

    def __init__(self, master=None, cnf={}, **kw):

        Toplevel.__init__(self, master, **kw)

        # app main window reference
        self.frm_master = master

        self.lstbox_ents = None
        self.edt_adb_path = None
        self.edt_json_syncdev = None
        self.edt_database_host = None
        self.edt_databaser_usr = None
        self.edt_database_port = None

        self.conf_frame = Frame(self, relief=RIDGE)
        self.conf_frame.pack(fill=BOTH, expand=1)

        # construct Configuration Form
        self.build_ini_form()

        # get main window position

        x = self.frm_master.master.winfo_x()
        y = self.frm_master.master.winfo_y()

        # update conf ini window properties
        self.update()

        # get conf ini window dimensions
        w = self.winfo_width()
        h = self.winfo_height()

        # set dimensions with 20px padding from main window
        self.geometry(
            '%dx%d+%d+%d' % (
                w, h,
                x - 20,
                y + 20
            )
        )

        # set conf ini title
        self.title('Configurações')

        self.edt_adb_path.focus()

    def build_ini_form(self):

        self.build_grp_box_ent()

        self.build_adb_path_widget()

        self.build_database_host_widget()

        self.build_database_usr_widget()

        self.build_database_port_widget()

        self.get_conf_ini_values()

        self.build_save_restore_frame()

    def build_grp_box_ent(self):

        # frame left side
        frm_syncdev_json = Frame(self.conf_frame)
        frm_syncdev_json.pack(side=TOP, fill=X, padx=3, pady=3)

        Label(frm_syncdev_json, text='Diretório syncdev(JSONs):').pack(side=LEFT)

        # Edit Mobile Path
        self.edt_json_syncdev = Entry(frm_syncdev_json, width=40, textvariable=self.frm_master.syncdev_json_path)
        self.edt_json_syncdev.pack(side=LEFT, fill=Y)

        # Button call dialog to look and get ADB Path
        Button(frm_syncdev_json, text='...', width=2, command=self.get_path_syncdev_json).pack(side=LEFT)

        frm_ents = Frame(self.conf_frame)
        frm_ents.pack(side=LEFT, fill=Y, padx=3, pady=3)

        Label(frm_ents, text='Entidades:').pack(anchor=NW, side=TOP, padx=2, pady=2)

        scrollbar = Scrollbar(frm_ents, orient=VERTICAL)

        self.lstbox_ents = Listbox(frm_ents, selectmode=EXTENDED, yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.lstbox_ents.yview)

        scrollbar.pack(side=RIGHT, fill=Y)

        self.lstbox_ents.pack(side=TOP)

    def build_adb_path_widget(self):

        # 1º frame row
        frm_row = Frame(self.conf_frame)
        frm_row.pack(side=TOP, pady=5, padx=2)

        Label(frm_row, text='ADB executável:').pack(side=LEFT)

        # Edit ADB Path
        self.edt_adb_path = Entry(frm_row, textvariable=self.frm_master.adb_path)
        self.edt_adb_path.pack(side=LEFT)

        # Button call dialog to look and get ADB Path
        Button(frm_row, text='...', width=2, command=self.get_path_to_adb_bin).pack(side=LEFT)

    def build_database_host_widget(self):

        frm_row = Frame(self.conf_frame)
        frm_row.pack(side=TOP, pady=5)

        Label(frm_row, text='Database host:').pack(side=LEFT)

        # Edit Mobile Path
        self.edt_database_host = Entry(frm_row, width=24, textvariable=self.frm_master.db_host)
        self.edt_database_host.pack(side=LEFT)

    def build_database_usr_widget(self):

        frm_row = Frame(self.conf_frame)
        frm_row.pack(side=TOP, pady=5)

        Label(frm_row, text='Database user:').pack(side=LEFT)

        # Edit Mobile Path
        self.edt_databaser_usr = Entry(frm_row, width=24, textvariable=self.frm_master.db_user)
        self.edt_databaser_usr.pack(side=LEFT)

    def build_database_port_widget(self):

        frm_row = Frame(self.conf_frame)
        frm_row.pack(side=TOP, pady=5)

        Label(frm_row, text='Database port:').pack(side=LEFT)

        # Edit Mobile Path
        self.edt_database_port = Entry(frm_row, width=24, textvariable=self.frm_master.db_port)
        self.edt_database_port.pack(side=LEFT)

    def build_lstbox_ents(self):

        for each_ent in self.frm_master.prefs_ini['Entities']:

            self.lstbox_ents.insert(END, each_ent)

            if self.frm_master.prefs_ini['Entities'].getboolean(each_ent):
                self.lstbox_ents.select_set(
                    self.lstbox_ents.size()-1
                )

                self.lstbox_ents.event_generate("<<ListboxSelect>>")

    def get_conf_ini_values(self):

        self.build_lstbox_ents()

        self.frm_master.adb_path.set(self.frm_master.prefs_ini['syncdev-Sync']['adb_bin'])

        self.frm_master.syncdev_json_path.set(self.frm_master.prefs_ini['syncdev-Sync']['syncdev_json'])

        self.frm_master.db_host.set(self.frm_master.prefs_ini['syncdev-PG']['server'])

        self.frm_master.db_user.set(self.frm_master.prefs_ini['syncdev-PG']['pg_user'])

        self.frm_master.db_port.set(self.frm_master.prefs_ini['syncdev-PG']['pg_port'])

    def build_save_restore_frame(self):

        frm_row = Frame(self.conf_frame)
        frm_row.pack(pady=5)

        Button(frm_row, text='Salvar', command=self.save_new_prefs_ini).pack(side=LEFT)

        Button(frm_row, text='Padrão', command=self.restore_default_conf_ini).pack(side=LEFT)

    def get_path_to_adb_bin(self):

        self.frm_master.adb_path.set(
            filedialog.askopenfilename()
        )

        self.lift()

        self.edt_adb_path.focus()

    def get_path_syncdev_json(self):

        self.frm_master.syncdev_json_path.set(
            filedialog.askdirectory()
        )

        self.load_entities_from_syncdev_json_path(self.frm_master.syncdev_json_path.get())

        self.lift()

        self.edt_json_syncdev.focus()

    def load_entities_from_syncdev_json_path(self, siason_directory):

        if not os.path.isdir(siason_directory):
            showerror('Diretório inválido', 'O diretório escolhido não é uma caminho válido')

        else:

            lst_jsons_syncdev = glob.glob(os.path.join(siason_directory,'*.json'))

            if not lst_jsons_syncdev:
                showerror('JSON não encontrado', 'Neste diretório não há arquivos JSONs.')

            else:

                for each_ent in lst_jsons_syncdev:

                    file_json_name = os.path.basename(each_ent)
                    file_json_name = file_json_name.replace('_', ' ')
                    file_json_name = file_json_name.replace('.json', '')

                    self.lstbox_ents.insert(END, file_json_name.title())

                    self.lstbox_ents.select_set(
                        self.lstbox_ents.size() - 1
                    )

                    self.lstbox_ents.event_generate("<<ListboxSelect>>")

    def save_new_prefs_ini(self):

        if askyesno('Configurações', 'Confirma gravação?'):
            new_prefs = configparser.ConfigParser()

            new_prefs.update({
                'syncdev-Sync': {
                    'adb_bin': self.frm_master.adb_path.get(),
                    'syncdev_json': self.frm_master.syncdev_json_path.get()
                },
                'Entities': {},
                'syncdev-PG': {
                    'server': self.frm_master.db_host.get(),
                    'pg_user': self.frm_master.db_user.get(),
                    'pg_port': self.frm_master.db_port.get()
                }
            })

            ini_bool = {
                True: 'yes',
                False: 'no'
            }

            for each_idx in range(0, self.lstbox_ents.size()):
                lstbox_id_ent = self.lstbox_ents.get(each_idx)
                new_prefs['Entities'][lstbox_id_ent] = ini_bool[self.lstbox_ents.select_includes(each_idx)]

            entidade_selecionada = verif_ha_entidade_selecionada(new_prefs)

            if not entidade_selecionada:
                if askyesno('Entidades', 'Não há nenhuma entidade selecionada. Deseja selecionar todas?'):
                    for each_idx in new_prefs['Entities']:
                        new_prefs['Entities'][each_idx] = 'yes'

            with open('./rsc/cnf/prefs.ini', 'w') as configfile:
                new_prefs.write(configfile)

            self.frm_master.prefs_ini = new_prefs

            self.destroy()
        else:

            self.lift()
            self.edt_adb_path.focus()

    def restore_default_conf_ini(self):

        if askyesno('Restaura padrão', 'Confirma restauração dos padrão?'):

            default_config = configparser.ConfigParser()

            default_config.update({
                'syncdev-Sync': {
                    'adb_bin': 'adb',
                    'syncdev_json': ''
                },
                'Entities': {},
                'syncdev-PG': {
                    'server': '',
                    'pg_user': '',
                    'pg_port': 5432
                }
            })

            with open('./rsc/cnf/prefs.ini', 'w') as configfile:
                default_config.write(configfile)

            self.frm_master.prefs_ini = default_config

            self.lstbox_ents.delete(0, END)

            self.get_conf_ini_values()

            showinfo(
                'Configurações restauradas',
                ''.join([
                    'Para o devido funcionamento',
                    ' da sincronização lembre-se de',
                    ' acessar esta janela e configurar',
                    ' novamente estes parâmetros'
                ])
            )

            self.destroy()
        else:
            self.lift()
            self.edt_adb_path.focus()
