"""
"""

from subprocess import check_output, CalledProcessError
from tkinter import DISABLED, END, NORMAL
from tkinter.messagebox import showerror, showinfo

from ctrl.core import valida_prefs_ini


def syncdev_para_movel(win_handle):

    resultado = valida_prefs_ini()

    # clean previous logging on Text Widget
    if len(win_handle.ety_log.get('1.0', 'end-1c')) > 0:
        win_handle.ety_log.config(state=NORMAL)
        win_handle.ety_log.delete(1.0, END)

    # validation result
    if not resultado['validacao']:
        showerror(
            resultado['erro-title'],
            resultado['erro-msg']
        )

        win_handle.ety_log.insert(END, 'Validação não efetuada com sucesso!\n')
        win_handle.ety_log.insert(
            END,
            ''.join([
                'Motivo:\n',
                resultado['erro-msg']
            ])
        )

        win_handle.ety_log.config(state=DISABLED)

    else:
        # starting syncronizing

        win_handle.ety_log.insert(END, 'Validação efetuada com sucesso!\n')

        win_handle.ety_log.insert(END, 'Inicializando serviço ADB!\n')

        # disable to prevent user input on Text widget
        win_handle.ety_log.config(state=DISABLED)

        out_msg = ''

        adb_tool = resultado['config']['syncdev-Sync']['adb_bin']

        try:
            out_msg = check_output(
                '{0} devices -l'.format(adb_tool),
                shell=True,
                universal_newlines=True
            )
        except CalledProcessError as e:
            win_handle.ety_log(
                'Erro ao inicializar serviço ADB! Retorno de sistema:{0}'.format(e)
            )
            exit()

        # enable to continue logging
        win_handle.ety_log.config(state=NORMAL)

        win_handle.ety_log.insert(
            END,
            ''.join([
                'Retorno do serviço ADB:\n',
                out_msg
            ])
        )

        # disable to prevent user input on Text widget
        win_handle.ety_log.config(state=DISABLED)

        showinfo(
            'Depuração USB',
            ''.join([
                'Prezado usuário,\n',
                'Conecte o seu dispositivo celular/tablet.\n',
                'Habilite a opção \'Depuração USB\'.\n'
                'Será emitido um aviso de conexão com o seu aparelho.\n',
                'Confirme esse aviso e clique em \'OK\' nesta janela para dar\n',
                'continuidade a sincronização.'
            ])
        )

        # testing adb syncing
        try:
            out_msg = check_output(
                '{0} push {1} /mnt/sdcard/'.format(adb_tool, resultado['config']['syncdev-Sync']['syncdev_json']),
                shell=True,
                universal_newlines=True
            )
        except CalledProcessError as e:
            win_handle.ety_log(
                'Erro ao inicializar serviço ADB! Retorno de sistema:{0}'.format(e)
            )
            exit()

        try:
            out_msg = check_output(
                '{0} kill-server'.format(adb_tool),
                shell=True,
                universal_newlines=True
            )
        except CalledProcessError as e:
            win_handle.ety_log(
                'Erro ao finalizar serviço ADB! Retorno de sistema:{0}'.format(e)
            )
            exit()

        # enable to continue logging
        win_handle.ety_log.config(state=NORMAL)

        win_handle.ety_log.insert(END, out_msg)

        win_handle.ety_log.insert(END, 'Sincronização finalizada!')

        win_handle.ety_log.config(state=DISABLED)
