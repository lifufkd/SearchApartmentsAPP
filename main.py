#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from modules.db import DB
from UI.visual_draw import UI
from modules.config_parser import ConfigParser
import flet as ft
import os
############static variables#####################
config_name = 'secrets.json'
#################################################

if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}')
    db = DB(config.get_config())
    ui = UI(config.get_config(), db)
    ft.app(target=ui.main, port=999, assets_dir=work_dir, view=ft.AppView.WEB_BROWSER)
    #view=ft.AppView.WEB_BROWSER