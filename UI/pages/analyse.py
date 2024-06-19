#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import PageData
from modules.CRUD import CRUD
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


############static variables#####################
class Analyse:
    def __init__(self, db):
        super(Analyse, self).__init__()
        self.__crud = CRUD(db)
        self.__table = None
        self.__chart = None
        self.__chart2 = None

    def analyse(self, pg: PageData):

        ### BUTTON FUNCTIONS ###
        def mainpage(e):
            pg.navigator.navigate('main', pg.page)

        def analyse_function(e):
            pg.navigator.navigate('analyse', pg.page)

        def go_to_site(e):
            pg.page.launch_url(url=e.control.tooltip)

        def prognoze_cost_week(e):
            data = {'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'price': [100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000]}
            df = pd.DataFrame(data)
            X_train, X_test, y_train, y_test = train_test_split(df[['week']], df['price'], test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, y_train)
            week_prediction = model.predict([[11]])[0]

            print(f"Прогноз цены через неделю: {week_prediction}")

        def prognoze_cost_month(e):
            data = {'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'price': [100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000]}
            df = pd.DataFrame(data)
            X_train, X_test, y_train, y_test = train_test_split(df[['week']], df['price'], test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, y_train)
            month_prediction = model.predict([[11 * 4]])[0]
            print(f"Прогноз цены через месяц: {month_prediction}")

        def prognoze_cost_year(e):
            data = {'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'price': [100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000]}
            df = pd.DataFrame(data)
            X_train, X_test, y_train, y_test = train_test_split(df[['week']], df['price'], test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, y_train)
            year_prediction = model.predict([[11 * 52]])[0]
            print(f"Прогноз цены через год: {year_prediction}")

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

        ### CHART ###

        def load_chart_info(flag, restrictions=None):
            if not flag:
                data = self.__crud.get_basic_query()
            else:
                data = self.__crud.get_restricted_query(restrictions)
            for row in data:
                self.__chart(ft.BarChartGroup(
                    x=row[0],
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=40,
                            color=ft.colors.AMBER,
                            tooltip=row[2],
                            border_radius=0,
                        ),
                    ]
                ))

        self.__chart = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.BLACK),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Цена Авито"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Apple"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("Blueberry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("Cherry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("Orange"), padding=10)
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            max_y=100,
            expand=True,
            bgcolor=ft.colors.GREY_700
        )

        load_chart_info(False)

        self.__chart2 = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=40,
                            color=ft.colors.AMBER,
                            tooltip="Apple",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=100,
                            width=40,
                            color=ft.colors.BLUE,
                            tooltip="Blueberry",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=30,
                            width=40,
                            color=ft.colors.RED,
                            tooltip="Cherry",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=3,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=60,
                            width=40,
                            color=ft.colors.ORANGE,
                            tooltip="Orange",
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.colors.BLACK),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Цена Циан"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Apple"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("Blueberry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("Cherry"), padding=10)
                    ),
                    ft.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("Orange"), padding=10)
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            max_y=100,
            expand=True,
            bgcolor=ft.colors.GREY_700,
        )

        ### BUTTONS ###
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)
        analys_button = ft.FilledButton(text='Анализ по агрегаторам', width=230, height=32, on_click=analyse_function)
        update_button = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text='Прогнозирование цены', disabled=True),
                ft.Divider(thickness=3),
                ft.PopupMenuItem(text='Через неделю', on_click=prognoze_cost_week),
                ft.PopupMenuItem(text='Через месяц', on_click=prognoze_cost_month),
                ft.PopupMenuItem(text='Через год', on_click=prognoze_cost_year),
            ]
        )

        ### TEXT ###
        logo_text = ft.Text(value='RealtorParser',
                            text_align=ft.TextAlign.LEFT, size=36, color='black')

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
                    analys_button,
                    update_button
                ],
                ),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row([
                self.__chart, self.__chart2
            ]),
            ft.Row([
                self.__table,
            ],
                scroll="always",
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
