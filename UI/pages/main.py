#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import PageData
from modules.CRUD import CRUD
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
############static variables#####################

#################################################


class MainPage:
    def __init__(self, db):
        super(MainPage, self).__init__()
        self.__bs = None
        self.__table = None
        self.__crud = CRUD(db)
        self.__comment_place = ft.TextField(label="Напишите комментарий")
        self.__filter_fields = [
                            ft.TextField(label='Город'),
                            ft.TextField(label='Площадь'),
                            ft.TextField(label='Цена'),
                            ft.TextField(label='Этаж')
                        ]

    def main_page(self, pg: PageData):
        def send_msg(e):
            # Записываем комментарий
            self.__crud.add_comment_by_id(e.control.tooltip, self.__comment_place.value, pg.page.session.get("creds"))
            close_comment(None)

        def studio_btns(e):
            pg.page.session.set('rooms', e.control.text)

        def author(e):
            pg.page.session.set('seller', e.control.text)

        def analyse_function(e):
            pg.navigator.navigate('analyse', pg.page)

        def apartaments(e):
            pg.navigator.navigate('apartaments', pg.page)
        def apartaments_pass(e):
            pg.navigator.navigate('apartaments_pass', pg.page)
        def vacation_home(e):
            pg.navigator.navigate('vacation_home', pg.page)

        def mainpage(e):
            pg.navigator.navigate('main', pg.page)

        def close_dlg(e):
            inputs = ['rooms', 'seller'] + self.__filter_fields
            restriction = list()
            for index, input in enumerate(inputs):
                if index in [0, 1]:
                    if pg.page.session.contains_key(input):
                        if pg.page.session.get(input) != 'не выбрано':
                            restriction.append(pg.page.session.get(input))
                        else:
                            restriction.append(False)
                    else:
                        restriction.append(False)
                    dlg_modal.open = False
                else:
                    if len(input.value) > 0:
                        if index in [3, 5]:
                            try:
                                restriction.append(float(input.value))
                            except:
                                restriction.append(False)
                                input.value = 'Ошибка! Не числовой формат'
                        else:
                            restriction.append(input.value)
                    else:
                        restriction.append(False)
            self.__table.rows.clear()
            if len(set(restriction)) == 1:
                print(323)
                load_table_info(False)
            else:
                load_table_info(True, restriction)
            pg.page.update()

        def load_table_info(flag, restrictions=None):
            if not flag:
                data = self.__crud.get_all_datas(50, "Купить")
            else:
                data = self.__crud.get_restricted_query(restrictions, "Купить")
            for row in data:
                self.__table.rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[2])),
                        ft.DataCell(ft.Text(row[3])),
                        ft.DataCell(ft.Text(row[4])),
                        ft.DataCell(ft.Text(row[5])),
                        ft.DataCell(ft.Text(row[6])),
                        ft.DataCell(ft.Text(row[7])),
                        ft.DataCell(ft.TextButton(text=row[8], tooltip=row[1], on_click=go_to_site)),
                        ft.DataCell(ft.IconButton(icon='COMMENT', tooltip=row[0], on_click=load_comments)),
                    ],
                ),
                )

        def load_comments(e):
            insert_comments(e.control.tooltip)
            pg.page.dialog = self.__bs
            self.__bs.open = True
            pg.page.update()

        def close_comment(e):
            self.__bs.open = False
            pg.page.update()

        def go_to_site(e):
            pg.page.launch_url(url=e.control.tooltip)


        def insert_comments(row_id):
            cart = list()
            cart.append(ft.Row([ft.Text("Комментарии                                                 ", size=24),
                                    ft.FilledButton(text="Закрыть", icon="CLOSE", on_click=close_comment)]))
            for i in self.__crud.get_comments_by_id(row_id):
                cart.append(ft.Text(i, size=16))
            cart.append(self.__comment_place)
            cart.append(ft.OutlinedButton(text="Отправить", icon="SEND", on_click=send_msg, tooltip=row_id))
            self.__bs = ft.BottomSheet(
                ft.Container(
                    ft.Column(
                        cart,
                        tight=True,
                    ),
                    padding=10,
                    border_radius=1,
                ),
                open=False,
            )

        def open_dlg_modal(e):
            pg.page.dialog = dlg_modal
            dlg_modal.open = True
            pg.page.update()


        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Фильтр"),
            content=ft.Column(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(value='Комнаты:', size=12),
                                    ft.FilledButton(text='не выбрано', on_click=studio_btns),
                                    ft.FilledButton(text='Студия', on_click=studio_btns),
                                    ft.FilledButton(text="1", on_click=studio_btns),
                                    ft.FilledButton(text="2", on_click=studio_btns),
                                    ft.FilledButton(text="3", on_click=studio_btns),
                                    ft.FilledButton(text="4+", on_click=studio_btns)
                                ]
                            ),
                            ft.Row([
                                ft.Text(value='Автор', size=12),
                                ft.FilledButton(text="Частное лицо", on_click=author),
                                ft.FilledButton(text="Риелтор", on_click=author)
                            ])
                        ]
                    ),
                    ft.Column(
                        self.__filter_fields
                    )
                ]
            ),
            actions=[
                ft.TextButton("Подтвердить", on_click=close_dlg),
            ],
        )

        pg.page.title = "Главная страница"
        pg.page.bgcolor = "#828282"  # Установить белый цвет фона страницы
        pg.page.vertical_alignment = "center"
        pg.page.horizontal_alignment = "center"
        pg.page.scroll = 'always'

        logo_text = ft.Text(value='RealtorParser',
                            text_align=ft.TextAlign.LEFT, size=36, color='black')
        parser_button = ft.FilledButton(text='Главная страница', width=170, height=32, on_click=mainpage)
        analys_button = ft.FilledButton(text='Анализ по агрегаторам', width=280, height=32, on_click=analyse_function)

        home_button = ft.FilledButton(text='Квартиры', on_click=apartaments)
        home_arenda_button = ft.FilledButton(text='Квартиры (сдать)', on_click=apartaments_pass)
        home_city_button = ft.FilledButton(text='Загородная недвижимость', on_click=vacation_home)
        filter_button = ft.FilledButton(text='Фильтр', icon="SETTINGS", on_click=open_dlg_modal)

        self.__table = ft.DataTable(
            border=ft.border.all(2, "white"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, "black"),
            horizontal_lines=ft.border.BorderSide(1, "black"),
            columns=[
                ft.DataColumn(ft.Text("Город")),
                ft.DataColumn(ft.Text("Этаж"), numeric=True),
                ft.DataColumn(ft.Text("Площадь"), numeric=True),
                ft.DataColumn(ft.Text("Комнаты"), numeric=True),
                ft.DataColumn(ft.Text("Цена"), numeric=True),
                ft.DataColumn(ft.Text("Опубликован")),
                ft.DataColumn(ft.Text("Сайт")),
                ft.DataColumn(ft.Text("")),
            ]
        )
        load_table_info(False)
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
                home_button, home_arenda_button, home_city_button
            ],
            ),
            ft.Row([
                filter_button,
            ],
            ),
            ft.Row([
                self.__table,
            ],
                scroll="always",
                alignment=ft.MainAxisAlignment.CENTER
            ),
        )