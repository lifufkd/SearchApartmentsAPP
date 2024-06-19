#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from flet_navigator import PageData
from modules.CRUD import CRUD


############static variables#####################
class Diagram(ft.UserControl):
    def __init__(self, diagram_data):
        super().__init__()
        self.__content = {1: ['База услуг', 'КСГ', 'МКБ', 'Услуги'], 2: ['Справочники', 'Регионы', 'Области', 'Мед. профили']}
        self.__diagram_data = diagram_data

    def add_diagram(self, cont, data):
        fig, ax = plt.subplots()
        plt.style.use('dark_background')
        fruits = [self.__content[cont][1], self.__content[cont][2], self.__content[cont][3]]
        counts = [data[0], data[1], data[2]]
        bar_colors = ["tab:red", "tab:blue", "tab:orange"]
        if cont == 3:
            fruits.append(self.__content[cont][4])
            counts.append(data[3])
            bar_colors.append('tab:green')
        ax.bar(fruits, counts, color=bar_colors)
        ax.set_title(self.__content[cont][0])
        return fig

    def build(self):
        return ft.Container(
            height=1500,
            content=ft.Row([
                        ft.Container(
                            height=450,
                            width=450,
                            content=MatplotlibChart(self.add_diagram(1, [self.__diagram_data['ksg'],
                                                                                   self.__diagram_data['mkb'],
                                                                                   self.__diagram_data['service']])),
                        ),
                        ft.Container(
                            height=450,
                            width=450,
                            content=MatplotlibChart(self.add_diagram(2, [self.__diagram_data['region'],
                                                                                   self.__diagram_data['area'],
                                                                                   self.__diagram_data['med_profile']])),
                        ),
                        ],
                        expand=True,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
        )


class Analyse:
    def __init__(self, db):
        super(Analyse, self).__init__()
        self.__crud = CRUD(db)
        self.__table = None

    def analyse(self, pg: PageData):

        ### BUTTON FUNCTIONS ###
        def mainpage(e):
            pg.navigator.navigate('main', pg.page)

        def analyse_function(e):
            pg.navigator.navigate('analyse', pg.page)

        def go_to_site(e):
            pg.page.launch_url(url=e.control.tooltip)

        ### LINECHART ###

            # linechart here

        ### TABLE ###
        def load_table_info(flag, restrictions=None):
            if not flag:
                data = self.__crud.get_basic_query()
            else:
                data = self.__crud.get_restricted_query(restrictions)
            for row in data:
                self.__table.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[6])),
                        ft.DataCell(ft.Text(row[7])),
                        ft.DataCell(ft.TextButton(text=row[8], tooltip=row[1], on_click=go_to_site)),
                    ],
                ),
                )

        self.__table = ft.DataTable(
            border=ft.border.all(2, "white"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, "black"),
            horizontal_lines=ft.border.BorderSide(1, "black"),
            columns=[
                ft.DataColumn(ft.Text("Адрес")),
                ft.DataColumn(ft.Text("Цена")),
                ft.DataColumn(ft.Text("Опубликован")),
                ft.DataColumn(ft.Text("Сайт")),
            ]
        )
        load_table_info(False)

        ### BUTTONS ###
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)

        ### TEXT ###
        logo_text = ft.Text(value='RealtorParser',
                            text_align=ft.TextAlign.LEFT, size=36, color='black')
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)
        analys_button = ft.FilledButton(text='Анализ по агрегаторам', width=280, height=32, on_click=analyse_function)

        ### PAGE SETTINGS ###
        pg.page.title = "Анализ по агрегаторам"
        pg.page.bgcolor = "#828282"  # Установить белый цвет фона страницы
        pg.page.vertical_alignment = "center"
        pg.page.horizontal_alignment = "center"
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
            ft.Row([
                ft.Container(
                    border_radius=10,
                    expand=True,
                    content=ft.Text('тут короче диаграмма будет'),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.BLUE_GREY_300,
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER,
                    )
                ),
                ]),
            ft.Row([
                self.__table,
            ],
                scroll="always",
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
