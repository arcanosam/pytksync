"""
"""
import configparser
import os
import pathlib
from tkinter.simpledialog import askstring

import psycopg2


def verif_ha_entidade_selecionada(cfg_ini_file):

    for each_ent in cfg_ini_file['Entities']:

        if cfg_ini_file['Entities'].getboolean(each_ent):
            return True

    return False


def valida_prefs_ini():

    cfg_ini_file = configparser.ConfigParser()

    cfg_ini_file.read('./rsc/cnf/prefs.ini')

    adb_file = pathlib.Path(cfg_ini_file['syncdev-Sync']['adb_bin'])

    if not adb_file.is_file():
        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: ADB Executável',
            'erro-msg': ''.join([
                'O campo "ADB Executável" na',
                ' janela de configurações é inválido ou não está preenchido.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    if len(cfg_ini_file['syncdev-Sync']['syncdev_json'].strip()) == 0 \
            or not os.path.isdir(cfg_ini_file['syncdev-Sync']['syncdev_json']):

        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: Diretório syncdev(JSONs)',
            'erro-msg': ''.join([
                'O campo "Diretório syncdev(JSONs)" na',
                ' janela de configurações é inválido ou não está preenchido.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    if len(cfg_ini_file['Entities'].keys()) == 0:
        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: Entidades',
            'erro-msg': ''.join([
                'O campo "Entidades" (lista de entidades) na',
                ' janela de configurações está vazio.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    else:

        entidade_selecionada = verif_ha_entidade_selecionada(cfg_ini_file)

        if not entidade_selecionada:
            return {
                'validacao': False,
                'erro-title': 'Erro - Configuração: Entidades',
                'erro-msg': ''.join([
                    'O campo "Entidades" (lista de entidades) na',
                    ' janela de configurações não possui nenhuma entidade selecionada.\n',
                    'Favor reveja as configurações em: Preferências --> Configurações'
                ])
            }

    if len(cfg_ini_file['syncdev-PG']['server'].strip()) == 0:
        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: DB Host',
            'erro-msg': ''.join([
                'O campo "Database host" na',
                ' janela de configurações não está preenchido.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    if len(cfg_ini_file['syncdev-PG']['pg_user'].strip()) == 0:
        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: DB User',
            'erro-msg': ''.join([
                'O campo "Database user" na',
                ' janela de configurações não está preenchido.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    if len(cfg_ini_file['syncdev-PG']['pg_port'].strip()) == 0:
        return {
            'validacao': False,
            'erro-title': 'Erro - Configuração: DB Port',
            'erro-msg': ''.join([
                'O campo "Database port" na',
                ' janela de configurações não está preenchido.\n',
                'Favor reveja as configurações em: Preferências --> Configurações'
            ])
        }

    pg_pwd = askstring('Teste de conexão', 'Digite a senha para teste de conexão com o banco:', show='*')

    try:
        conn_test = psycopg2.connect(
            dbname='postgres',
            user=cfg_ini_file['syncdev-PG']['pg_user'],
            host=cfg_ini_file['syncdev-PG']['server'],
            password=pg_pwd,
            port=cfg_ini_file['syncdev-PG']['pg_port']
        )
    except psycopg2.OperationalError as e:
        return {
            'validacao': False,
            'erro-title': 'Erro - Teste de conexão',
            'erro-msg': ''.join([
                'O teste de conexão com o banco de dados falhou.',
                ' Favor reveja as configurações em: Preferências --> Configurações\n',
                ' Mensagem de sistema: {0}'.format(e)
            ])
        }

    conn_test = None

    return {
        'validacao': True,
        'config': cfg_ini_file
    }
