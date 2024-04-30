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
from modules.utilites import unparse_json, update_data_area, update_data_hospital, insert_data_hospital


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
        data = self.__process_data.hospital(self.__data)
        print(data)
        if self.__row_id is None:
            try:
                insert_data_hospital(self.__db, data)
                self.init_dlg(True)
            except Exception as e:
                print(e)
                self.init_dlg(False)
        else:
            try:
                update_data_hospital(self.__db, data, self.__row_id)
                self.init_dlg(True)
            except Exception as e:
                print(e)
                self.init_dlg(False)

    def init_dlg(self, switch):
        if switch:
            self.dlg_modal(['Данные успешно сохранены!', 'god damn right'])
            self.open_dlg_modal(None)
        else:
            self.dlg_modal(['Данные не сохранены', 'дополните заявку'])
            self.open_dlg_modal(None)

    def existed_data(self):
        return self.__load_pages.hospital(self.__row_id)

    def user(self):
        carts = list()
        fios = list()
        for fio in self.__load_drop_box.close_author():
            user_fio = unparse_json(fio[0])
            fios.append([f'{user_fio[0]} {user_fio[1]} {user_fio[2]}', fio[1]])
        for cart in fios:
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def load_region(self):
        carts = list()
        for cart in self.__load_drop_box.region():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def load_area(self):
        carts = list()
        for cart in self.__load_drop_box.area():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def build(self):
        if self.__row_id is not None:
            self.__existed_data = self.existed_data()
            print(self.__existed_data)
        else:
            for x in range(30):
                if x == 3:
                    self.__existed_data.append(self.__load_drop_box.base_ratio()[0][0])
                elif x == 4:
                    self.__existed_data.append(self.__load_drop_box.base_vote()[0][0])
                else:
                    self.__existed_data.append('')
        self.__data[0] = TextField(label='Название', value=self.__existed_data[0])
        self.__data[1] = TextField(label='Медицинские профили (ввод через запятую)', value=self.__existed_data[1])
        self.__data[2] = Dropdown(hint_text='Модератор', options=self.user(), value=self.__existed_data[2])
        self.__data[3] = TextField(label="Коэффициент дифференциации", value=self.__existed_data[3], suffix_text="В формате 9.99 (не >9.99)")
        self.__data[4] = TextField(label="Базовая ставка", value=self.__existed_data[4], suffix_text="В формате 99999.99 (не >99999.99)")
        self.__data[5] = TextField(label="Сайт", value=self.__existed_data[5], prefix_text="https://", suffix_text=".com")
        self.__data[6] = TextField(label="Телефон", value=self.__existed_data[6], prefix_text="+7")
        self.__data[7] = TextField(label="E-mail", value=self.__existed_data[7])
        self.__data[8] = TextField(label="Тип", value=self.__existed_data[8])
        self.__data[9] = TextField(label="Значение", value=self.__existed_data[9])
        self.__data[10] = TextField(label="Тип", value=self.__existed_data[10])
        self.__data[11] = TextField(label="Значение", value=self.__existed_data[11])
        self.__data[12] = TextField(label="Тип", value=self.__existed_data[12])
        self.__data[13] = TextField(label="Значение", value=self.__existed_data[13])
        self.__data[14] = Dropdown(hint_text='Регион', options=self.load_region(), value=self.__existed_data[14])
        self.__data[15] = Dropdown(hint_text='Область', options=self.load_area(), value=self.__existed_data[15])
        self.__data[16] = TextField(label="Город", value=self.__existed_data[16])
        self.__data[17] = TextField(label="Адрес", value=self.__existed_data[17])
        self.__data[18] = TextField(label="Номер договора", value=self.__existed_data[18])
        self.__data[19] = TextField(label="Управляющий клиники", value=self.__existed_data[19])
        self.__data[20] = TextField(label="Должность управляющего", value=self.__existed_data[20])
        self.__data[21] = TextField(label="ФИО управляющего", value=self.__existed_data[21])
        self.__data[22] = TextField(label="ИНН", value=self.__existed_data[22])
        self.__data[23] = TextField(label="КПП", value=self.__existed_data[23])
        self.__data[24] = TextField(label="ОГРН", value=self.__existed_data[24])
        self.__data[25] = TextField(label="Почтовый индекс", value=self.__existed_data[25])
        self.__data[26] = TextField(label="Расчётный счёт", value=self.__existed_data[26])
        self.__data[27] = TextField(label="Название банка", value=self.__existed_data[27])
        self.__data[28] = TextField(label="Корреспондентский счет", value=self.__existed_data[28])
        self.__data[29] = TextField(label="БИК", value=self.__existed_data[29])
        self.__data[30] = FilledButton(text='Сохранить', on_click=self.save_changes)
        other_contacts = DataTable(
            vertical_lines=border.BorderSide(1),
            horizontal_lines=border.BorderSide(1),
            data_row_min_height=0,
            data_row_max_height=200,
            show_bottom_border=True,
            width=1600,
            border_radius=10,
            border=border.all(2, "black"),
            columns=[
                DataColumn(Text("#")),
                DataColumn(Text("Тип")),
                DataColumn(Text("Значение")),
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text(value="1")),
                        DataCell(self.__data[8]),
                        DataCell(self.__data[9]),
                ]
                ),
                DataRow(
                    cells=[
                        DataCell(Text(value="2")),
                        DataCell(self.__data[10]),
                        DataCell(self.__data[11]),
                    ]
                ),
                DataRow(
                    cells=[
                        DataCell(Text(value="3")),
                        DataCell(self.__data[12]),
                        DataCell(self.__data[13]),
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
                            Text(value='Информация о заявке', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Divider(height=10),
                        Container(
                            Text(value='Базовые', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[0], padding=padding.only(left=50, right=50)),
                        Container(self.__data[1], padding=padding.only(left=50, right=50)),
                        Container(self.__data[2], padding=padding.only(left=50, right=50)),
                        Container(self.__data[3], padding=padding.only(left=50, right=50)),
                        Container(self.__data[4], padding=padding.only(left=50, right=50)),
                        Divider(height=19),
                        Container(
                            Text(value='Контакты', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[5], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[6], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[7], padding=padding.only(left=50, right=50, top=10)),
                        Container(other_contacts, padding=padding.only(left=50, right=50, top=10)),
                        Divider(height=10),
                        Container(
                            Text(value='Расположение', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[14], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[15], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[16], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[17], padding=padding.only(left=50, right=50, top=10)),
                        Divider(height=10),
                        Container(
                            Text(value='Реквизиты', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[18], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[19], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[20], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[21], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[22], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[23], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[24], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[25], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[26], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[27], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[28], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[29], padding=padding.only(left=50, right=50, top=10)),
                        Container(self.__data[30], padding=padding.only(left=50, right=50, top=10, bottom=10)),
                    ],
                    scroll=ScrollMode.ALWAYS,
                    )
                )
            )
        )

class change_clinics:
    def __init__(self, vault, config, db):
        super(change_clinics, self).__init__()
        self.__ogrn7 = None
        self.__ogrn6 = None
        self.__ogrn5 = None
        self.__ogrn2 = None
        self.__ogrn4 = None
        self.__ogrn3 = None
        self.__ogrn1 = None
        self.__save = None
        self.__bik = None
        self.__correspondent_account = None
        self.__bank_name = None
        self.__postcode = None
        self.__ogrn = None
        self.__kpp = None
        self.__tin = None
        self.__position_manager = None
        self.__clinic_manager = None
        self.__contract_number = None
        self.__address = None
        self.__city = None
        self.__area = None
        self.__region = None
        self.__other_contacts = None
        self.__email = None
        self.__phone = None
        self.__phone = None
        self.__site = None
        self.__base_rate = None
        self.__diff_coefficient = None
        self.__moderator = None
        self.__medical_profiles = None
        self.__name = None
        self.__states = None
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_drop_box = LoadDropBox(db)
        self.__load_pages = LoadPages(db)
        self.__process_data = ProcessData()
        self.__data_buttons = [self.__name, self.__medical_profiles, self.__moderator, self.__diff_coefficient,
                               self.__base_rate, self.__site, self.__phone, self.__email, self.__other_contacts,
                               self.__region, self.__area, self.__city, self.__address, self.__contract_number,
                               self.__clinic_manager, self.__position_manager, self.__tin, self.__kpp, self.__ogrn, self.__ogrn1, 
                               self.__ogrn2, self.__ogrn3, self.__ogrn4, self.__ogrn5, self.__ogrn6, self.__ogrn7,
                               self.__postcode, self.__bank_name, self.__correspondent_account, self.__bik, self.__save]


    def change_clinics(self, pg: PageData):
        row_id = pg.page.client_storage.get("current_action")[1]
        self.__states = {'add': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data),
                         'change': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db,
                                           self.__process_data, self.__load_pages, row_id)}
        if row_id is not None:
            name = 'изменить'
        else:
            name = 'создать'
        pg.page.title = f"Клиники - {name}"
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
                        )
                    )
                ],
                expand=True,
            )
        )
        pg.page.update()
