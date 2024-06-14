#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import PageData
from modules.CRUD import CRUD
############static variables#####################

#################################################


class Analyse:
    def __init__(self, db):
        super(Analyse, self).__init__()
        self.__crud = CRUD(db)

    def analyse(self, pg: PageData):

        ### BUTTON FUNCTIONS ###
        def mainpage(e):
            pg.navigator.navigate('main', pg.page)

        def analyse_function(e):
            pg.navigator.navigate('analyse', pg.page)


        ### BUTTONS ###
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)

        ### TEXT ###
        logo_text = ft.Text(value='RealtorParser',
                            text_align=ft.TextAlign.LEFT, size=36, color='black')
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)
        analys_button = ft.FilledButton(text='Анализ по агрегаторам', width=280, height=32, on_click=analyse_function)

        pg.page.title = "Главная страница"
        pg.page.bgcolor = "#828282"  # Установить белый цвет фона страницы
        pg.page.scroll = 'always'

        pg.page.add(
            ft.Row([
                ft.Row([
                    logo_text,
                ],
                ),
                ft.Row([
                    parser_button,
                    analys_button
                ],
                ),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )