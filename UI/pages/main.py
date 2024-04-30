#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from flet_navigator import PageData
from UI.sidebar import SideBar
from modules.utilites import get_data_main_page
#################################################


class Diagram(UserControl):
    def __init__(self, diagram_data):
        super().__init__()
        self.__content = {1: ['База услуг', 'КСГ', 'МКБ', 'Услуги'], 2: ['Справочники', 'Регионы', 'Области', 'Мед. профили'], 3: ['Пользователи', 'Админы', 'Кураторы', 'Модераторы', 'Пользователи']}
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
        return Container(
            height=1500,
            content=Row([
                        Container(
                            height=450,
                            width=450,
                            content=MatplotlibChart(self.add_diagram(1, [self.__diagram_data['ksg'],
                                                                                   self.__diagram_data['mkb'],
                                                                                   self.__diagram_data['service']])),
                        ),
                        Container(
                            height=450,
                            width=450,
                            content=MatplotlibChart(self.add_diagram(2, [self.__diagram_data['region'],
                                                                                   self.__diagram_data['area'],
                                                                                   self.__diagram_data['med_profile']])),
                        ),
                        Container(
                            height=450,
                            width=450,
                            content=MatplotlibChart(self.add_diagram(3, [self.__diagram_data['users'][0],
                                                                                   self.__diagram_data['users'][1],
                                                                                   self.__diagram_data['users'][2],
                                                                                   self.__diagram_data['users'][3]])),
                        ),
                        ],
                        expand=True,
                        vertical_alignment=CrossAxisAlignment.START,
                        alignment=MainAxisAlignment.SPACE_AROUND,
                    ),
        )


class Main:
    def __init__(self, vault, config, db):
        super(Main, self).__init__()
        self.__vault = vault
        self.__config = config
        self.__db = db

    def main(self, pg: PageData):
        pg.page.title = "Главное меню"
        pg.page.theme_mode = 'dark'
        pg.page.horizontal_alignment = "stretch"
        pg.page.vertical_alignment = "stretch"
        pg.page.add(
            Row(
                [
                Container(
                    border_radius=10,
                    content=SideBar(self.__vault, pg),
                    shadow=BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=colors.BLUE_GREY_300,
                        offset=Offset(0, 0),
                        blur_style=ShadowBlurStyle.OUTER,
                    )
                ),
                Container(
                    border_radius=10,
                    expand=True,
                    content=Diagram(get_data_main_page(self.__db)),
                    shadow=BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=colors.BLUE_GREY_300,
                        offset=Offset(0, 0),
                        blur_style=ShadowBlurStyle.OUTER,
                    )
                ),
            ],
                expand=True,
            )
        )
        pg.page.update()
        plt.close()