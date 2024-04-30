#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
from flet_navigator import PageData

from modules.load_data import LoadData
from modules.utilites import word_wrap, save_export_xlsx, delete_row
from UI.sidebar import SideBar
#################################################


class Content(UserControl):
    def __init__(self, load_data, db, pg):
        super().__init__()
        self.__load_data = load_data
        self.__db = db
        self.__pg = pg

    def build(self):
        return (Container
            (
            padding=padding.only(left=30, right=30, top=15),
            expand=True,
            content=Container
                (
                shadow=BoxShadow
                    (
                    spread_radius=0.5,
                    blur_radius=15,
                    color=colors.BLUE_GREY_300,
                    offset=Offset(0, 0),
                    blur_style=ShadowBlurStyle.OUTER,
                ),
                border_radius=10,
                content=Row(
                    [
                        DataTable(
                            vertical_lines=border.BorderSide(1),
                            horizontal_lines=border.BorderSide(1),
                            data_row_min_height=0,
                            data_row_max_height=200,
                            show_bottom_border=True,
                            width=1600,
                            columns=
                            [
                                DataColumn(Text(value='Название', size=15)),
                                DataColumn(Text(value='КСГ', size=15)),
                                DataColumn(Text(value='', size=15)),
                                DataColumn(Text(value='', size=15)),
                            ],
                            rows=self.generate_carts()
                        )
                    ]
                )
            )
        )
        )

    def delete_row(self, event):
        delete_row(self.__db, {'med_profile': ['id', event.control.tooltip], 'relative_ksg_med_profile': ['id_med_profile', event.control.tooltip]})
        self.__pg.page.update()

    def change(self, event):
        self.__pg.page.client_storage.set("current_action", ["change", event.control.tooltip])
        self.__pg.navigator.navigate('med_profile_change_med_profile', self.__pg.page)

    def generate_carts(self):
        carts = list()
        for cart in self.__load_data.med_profile():
            carts.append(
                DataRow(
                    cells=[
                        DataCell(Text(cart[0])),
                        DataCell(Text(cart[1])),
                        DataCell(IconButton(icon=icons.MODE_EDIT_OUTLINE_OUTLINED, tooltip=cart[2], on_click=self.change)),
                        DataCell(IconButton(icon=icons.DELETE, tooltip=cart[2], on_click=self.delete_row)),
                    ]
                )
            )
        return carts


class med_profile_ui(UserControl):
    def __init__(self, pg, load_data, config, db):
        super().__init__()
        self.__pg = pg
        self.__load_data = load_data
        self.__config = config
        self.__db = db

    def add(self, event):
        self.__pg.page.client_storage.set("current_action", ["add", None])
        self.__pg.navigator.navigate('med_profile_change_med_profile', self.__pg.page)

    def create_export(self, event):
        save_export_xlsx(self.__config['export_xlsx_path'], self.__load_data.med_profile(), 'med_profile')

    def build(self):
        # ЗНАЧЕНИЯ#
        btn_create = FilledButton(icon=icons.ADD,
                                  text='Создать', on_click=self.add)  # ЭТО КНОПКА ДЛЯ СОЗДАНИЯ ЗАЯВКИ, НУЖНО СДЕЛАТЬ ПЕРЕХОД С ЭТОЙ КНОПКИ НА ДРУГУЮ СТРАНИЦУ
        pb = PopupMenuButton(
            items=[
                PopupMenuItem(icon=icons.CLOUD_DOWNLOAD, text='Экспорт', on_click=self.create_export)
            ]
        )
        return Container(
            height=1500,
            content=Column(
                [
                    Container(
                        content=Text(value='Мед. профили', size=20),
                        padding=padding.only(left=60, right=60, top=20)
                    ),
                    Container(
                        content=Row([btn_create, pb]),
                        padding=padding.only(left=50, top=10),
                    ),
                    Container(
                        content=Content(self.__load_data, self.__db, self.__pg)
                    ),
                ],
                expand=True,
                scroll=ScrollMode.ALWAYS,
                alignment=MainAxisAlignment.START,
            ),
        )



class Med_profile:
    def __init__(self, vault, config, db):
        super(Med_profile, self).__init__()
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_data = LoadData(db)

    def med_profile(self, pg: PageData):
        pg.page.title = "Мед. профили"
        pg.page.theme_mode = 'dark'
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
                        content=med_profile_ui(pg, self.__load_data, self.__config, self.__db),
                        shadow=BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.BLUE_GREY_300,
                            offset=Offset(0, 0),
                            blur_style=ShadowBlurStyle.OUTER,
                        )
                    )
                ],
                expand=True,
            )
        )
        pg.page.update()