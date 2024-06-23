import flet as ft
from flet_navigator import PageData
from modules.CRUD import CRUD
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class Analyse:
    def __init__(self, db):
        super(Analyse, self).__init__()
        self.__crud = CRUD(db)
        self.__table = None
        self.__chart = None
        self.__chart2 = None

    def analyse(self, pg: PageData):

        def mainpage(e):
            pg.navigator.navigate('main', pg.page)

        def analyse_function(e):
            pg.navigator.navigate('analyse', pg.page)

        def go_to_site(e):
            pg.page.launch_url(url=e.control.tooltip)

        def prognoze_price(price, weeks_ahead):
            data = {'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'price': [100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000]}
            df = pd.DataFrame(data)
            df['price_diff'] = df['price'].diff().fillna(0)
            X_train, X_test, y_train, y_test = train_test_split(df[['week']], df['price_diff'], test_size=0.2)
            model = LinearRegression()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            predicted_increase = model.predict([[len(data['week']) + weeks_ahead]])[0]
            return price + predicted_increase

        def prognoze_price_week(price):
            return prognoze_price(price, 1)

        def prognoze_price_month(price):
            return prognoze_price(price, 4)

        def prognoze_price_year(price):
            return prognoze_price(price, 52)

        def prognoze_cost_week(e):
            database = self.__crud.get_all_datas(5)
            self.__table.rows.clear()
            for row in database:
                try:
                    price = int(row[6].replace('от ', '').replace('₽', '').replace(' ', ''))
                    new_price = prognoze_price_week(price)
                    new_price = round(new_price, 2)
                    self.__table.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(ft.Text(str(new_price))),
                            ft.DataCell(ft.Text(row[7])),
                            ft.DataCell(ft.TextButton(text=row[8], tooltip=row[1], on_click=go_to_site)),
                        ],
                    ),
                    )
                except:
                    continue
            pg.page.update()

        def prognoze_cost_month(e):
            database = self.__crud.get_all_datas(5)
            self.__table.rows.clear()
            for row in database:
                try:
                    price = int(row[6].replace('от ', '').replace('₽', '').replace(' ', ''))
                    new_price = prognoze_price_month(price)
                    self.__table.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(ft.Text(str(new_price))),
                            ft.DataCell(ft.Text(row[7])),
                            ft.DataCell(ft.TextButton(text=row[8], tooltip=row[1], on_click=go_to_site)),
                        ],
                    ),
                    )
                except:
                    continue
            pg.page.update()

        def prognoze_cost_year(e):
            database = self.__crud.get_all_datas(5)
            self.__table.rows.clear()
            for row in database:
                try:
                    price = int(row[6].replace('от ', '').replace('₽', '').replace(' ', ''))
                    new_price = prognoze_price_year(price)
                    self.__table.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row[2])),
                            ft.DataCell(ft.Text(str(new_price))),
                            ft.DataCell(ft.Text(row[7])),
                            ft.DataCell(ft.TextButton(text=row[8], tooltip=row[1], on_click=go_to_site)),
                        ],
                    ),
                    )
                except:
                    continue
            pg.page.update()

        def load_table_info(flag, restrictions=None):
            if not flag:
                data = self.__crud.get_all_datas(10)
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

        def load_chart_info_avito():
            data = self.__crud.get_avito_datas(10, None)
            self.__chart.bar_groups.clear()
            x_labels = []
            for index, datas in enumerate(data):
                try:
                    price = int(datas[6].replace('от ', '').replace('₽', '').replace(' ', ''))
                    if price > 100000:
                        price = 100000
                    self.__chart.bar_groups.append(
                        ft.BarChartGroup(
                            x=index,
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=price,
                                    width=40,
                                    color=ft.colors.AMBER,
                                    tooltip=datas[2],
                                    border_radius=0,
                                ),
                            ]
                        )
                    )
                    x_labels.append(ft.ChartAxisLabel(
                        value=index, label=ft.Container(ft.Text("Квартира"), padding=5)
                    ))
                except ValueError:
                    continue

            self.__chart.bottom_axis = ft.ChartAxis(
                labels=x_labels,
                labels_size=40,
            )

            pg.page.update()

        def load_chart_info_cian():
            data = self.__crud.get_cian_datas(10, None)
            self.__chart2.bar_groups.clear()
            x_labels = []
            for index, datas in enumerate(data):
                try:
                    price = int(datas[6].replace('от ', '').replace('₽', '').replace(' ', ''))
                    if price > 100000:
                        price = 100000
                    self.__chart2.bar_groups.append(
                        ft.BarChartGroup(
                            x=index,
                            bar_rods=[
                                ft.BarChartRod(
                                    from_y=0,
                                    to_y=price,
                                    width=40,
                                    color=ft.colors.AMBER,
                                    tooltip=datas[2],
                                    border_radius=0,
                                ),
                            ]
                        )
                    )
                    x_labels.append(ft.ChartAxisLabel(
                        value=index, label=ft.Container(ft.Text("Квартира"), padding=5)
                    ))
                except ValueError:
                    continue

            self.__chart2.bottom_axis = ft.ChartAxis(
                labels=x_labels,
                labels_size=40,
            )

            pg.page.update()

        self.__chart = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.BLACK),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Цена Авито"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            max_y=120000,
            expand=True,
            bgcolor=ft.colors.GREY_700
        )

        load_chart_info_avito()

        self.__chart2 = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.BLACK),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Цена Циан"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=[],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            max_y=120000,
            expand=True,
            bgcolor=ft.colors.GREY_700
        )

        load_chart_info_cian()

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

        logo_text = ft.Text(value='RealtorParser',
                            text_align=ft.TextAlign.LEFT, size=36, color='black')

        pg.page.title = "Анализ по агрегаторам"
        pg.page.bgcolor = "#828282"
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
