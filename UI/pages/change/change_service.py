#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
from flet_navigator import PageData
from UI.sidebar import SideBar
from modules.load_data import LoadDropBox, LoadPages
from modules.process_data import ProcessData
from modules.utilites import insert_data_service, update_data_service


#################################################


class Content(UserControl):
    def __init__(self, load_drop_box, buttons, pg, db, process_data, load_pages=None, row_id=None):
        super().__init__()
        self.__dlg_modal = None
        self.__existed_data = []
        self.__load_drop_box = load_drop_box
        self.__load_pages = load_pages
        self.__process_data = process_data
        self.__row_id = row_id
        self.__data = buttons
        self.__pg = pg
        self.__db = db

    def close_dlg(self, e):
        self.__dlg_modal.open = False
        self.__pg.page.update()

    def open_dlg_modal(self, e):
        self.__pg.page.dialog = self.__dlg_modal
        self.__dlg_modal.open = True
        self.__pg.page.update()

    def dlg_modal(self, data):
        self.__dlg_modal = AlertDialog(
            modal=True,
            title=Text(data[0]),
            content=Text(data[1]),
            actions=[
                TextButton("Ok", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def save_changes(self, e):
        data = self.__process_data.service(self.__data)
        if self.__row_id is None:
            try:
                insert_data_service(self.__db, data)
                self.init_dlg(True)
            except Exception as e:
                print(e)
                self.init_dlg(False)
        else:
            try:
                update_data_service(self.__db, data, self.__row_id)
                self.init_dlg(True)
            except:
                self.init_dlg(False)

    def init_dlg(self, switch):
        if switch:
            self.dlg_modal(['Данные успешно сохранены!', 'god damn right'])
            self.open_dlg_modal(None)
        else:
            self.dlg_modal(['Данные не сохранены', 'дополните заявку'])
            self.open_dlg_modal(None)

    def existed_data(self):
        return self.__load_pages.service(self.__row_id)

    def categories(self):
        carts = list()
        for cart in [["Лабораторные исследования", 0], ['Инструментальные исследования', 1], ['Консультации специалистов', 2]]:
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def build(self):
        if self.__row_id is not None:
            self.__existed_data = self.existed_data()
        else:
            for x in range(13):
                self.__existed_data.append('')
        self.__data[0] = TextField(label="Код", value=self.__existed_data[0])
        self.__data[1] = TextField(label="Название", value=self.__existed_data[1])
        self.__data[2] = TextField(label="МКБ", value=self.__existed_data[2])
        self.__data[3] = TextField(label="КСГ", value=self.__existed_data[3])
        self.__data[4] = Dropdown(hint_text='Категории', options=self.categories(), value=self.__existed_data[4])
        self.__data[5] = TextField(label="Название", value=self.__existed_data[5])
        self.__data[6] = TextField(label="Время действия (Дней)", value=self.__existed_data[6])
        self.__data[7] = Dropdown(hint_text='Категории', options=self.categories(), value=self.__existed_data[7])
        self.__data[8] = TextField(label="Название", value=self.__existed_data[8])
        self.__data[9] = TextField(label="Время действия (Дней)", value=self.__existed_data[9])
        self.__data[10] = Dropdown(hint_text='Категории', options=self.categories(), value=self.__existed_data[10])
        self.__data[11] = TextField(label="Название", value=self.__existed_data[11])
        self.__data[12] = TextField(label="Время действия (Дней)", value=self.__existed_data[12])
        self.__data[13] = FilledButton(text='Сохранить', on_click=self.save_changes)
        clinical_minimum = DataTable(
            border_radius=10,
            width=1500,
            border=border.all(2, "black"),
            columns=[
                DataColumn(Text("#")),
                DataColumn(Text("Категории")),
                DataColumn(Text("Название")),
                DataColumn(Text("Время действия (Дней)")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(value="1")),
                        DataCell(self.__data[4]),
                        DataCell(self.__data[5]),
                        DataCell(self.__data[6]),
                    ]
                ),
                DataRow(
                    cells=[
                        DataCell(Text(value="2")),
                        DataCell(self.__data[7]),
                        DataCell(self.__data[8]),
                        DataCell(self.__data[9]),
                    ]
                ),
                DataRow(
                    cells=[
                        DataCell(Text(value="3")),
                        DataCell(self.__data[10]),
                        DataCell(self.__data[11]),
                        DataCell(self.__data[12]),
                    ]
                )
            ]
        )
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
                content=Column(
                    [
                        Container(
                            Text(value='Услуги - Создать', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Divider(height=10),
                        Container(self.__data[0], padding=padding.only(left=50, right=50)),
                        Container(self.__data[1], padding=padding.only(left=50, right=50)),
                        Container(self.__data[2], padding=padding.only(left=50, right=50)),
                        Container(self.__data[3], padding=padding.only(left=50, right=50)),
                        Container(
                            Text(value='Клинический минимум', size=14),
                            padding=padding.only(left=50, right=50, top=5, bottom=2),
                        ),
                        Container(clinical_minimum, padding=padding.only(left=50, right=50)),
                        Container(self.__data[13], padding=padding.only(left=50, right=50, top=10, bottom=10)),
                    ],
                    )
                )
            )
        )
class change_service:
    def __init__(self, vault, config, db):
        super(change_service, self).__init__()
        self.__param9 = None
        self.__param8 = None
        self.__param7 = None
        self.__param2 = None
        self.__param6 = None
        self.__param5 = None
        self.__param1 = None
        self.__param4 = None
        self.__param3 = None
        self.__save = None
        self.__csg = None
        self.__mkb = None
        self.__name = None
        self.__code = None
        self.__states = None
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_drop_box = LoadDropBox(db)
        self.__load_pages = LoadPages(db)
        self.__process_data = ProcessData()
        self.__data_buttons = [self.__code, self.__name, self.__mkb, self.__csg, self.__param1, self.__param2, 
                               self.__param3, self.__param4, self.__param5, self.__param6, self.__param7, self.__param8, 
                               self.__param9, self.__save]

    def change_service(self, pg: PageData):
        row_id = pg.page.client_storage.get("current_action")[1]
        self.__states = {'add': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data),
                         'change': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db,
                                           self.__process_data, self.__load_pages, row_id)}
        if row_id is not None:
            name = 'изменить'
        else:
            name = 'создать'
        pg.page.title = f"Услуги - {name}"
        pg.page.theme_mode = 'dark'
        pg.page.vertical_alignment = MainAxisAlignment.CENTER
        pg.page.horizontal_alignment = CrossAxisAlignment.CENTER
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
                        content=self.__states[pg.page.client_storage.get("current_action")[0]],
                        shadow=BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=colors.BLUE_GREY_300,
                            offset=Offset(0, 0),
                            blur_style=ShadowBlurStyle.OUTER,
                        ),
                    )
                ],
                expand=True,
            )
        )
        pg.page.update()
