#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from datetime import datetime
from flet import *
from flet_navigator import PageData
from UI.sidebar import SideBar
from modules.load_data import LoadDropBox, LoadPages
from modules.utilites import insert_data_application, unparse_json, update_data_application
from modules.process_data import ProcessData
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
        data = self.__process_data.application(self.__data)
        print(data)
        if self.__row_id is None:
            try:
                insert_data_application(self.__db, 'application', data)
                self.init_dlg(True)
            except:
                self.init_dlg(False)
        else:
            try:
                update_data_application(self.__db, 'application', data, self.__row_id)
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

    def load_application_type(self):
        carts = list()
        for cart in self.__load_drop_box.load_application_type():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def payment_type(self):
        carts = list()
        for cart in self.__load_drop_box.load_payment_type():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def status(self):
        carts = list()
        for cart in self.__load_drop_box.application_status():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def close_author(self):
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

    def mkb(self):
        carts = list()
        for cart in self.__load_drop_box.mkb():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def service(self):
        carts = list()
        for cart in self.__load_drop_box.service():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def hospitalized(self):
        carts = list()
        for cart in self.__load_drop_box.hospitalized():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def hospital(self):
        carts = list()
        for cart in self.__load_drop_box.hospital():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def benefit_status(self):
        carts = list()
        for cart in self.__load_drop_box.benefit_status():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def existed_data(self):
        return self.__load_pages.application(self.__row_id)

    def build(self):
        if self.__row_id is not None:
            self.__existed_data = self.existed_data()
        else:
            for x in range(22):
                self.__existed_data.append('')
        self.__data[0] = TextField(label='Номер', value=self.__existed_data[0])
        self.__data[1] = Dropdown(hint_text='Тип заявки', options=self.load_application_type(), value=self.__existed_data[1])
        self.__data[2] = Dropdown(hint_text='Тип оплаты', options=self.payment_type(), value=self.__existed_data[2])
        self.__data[3] = Dropdown(hint_text='Статус заявки', options=self.status(), value=self.__existed_data[3])
        self.__data[4] = Dropdown(hint_text='Автор закрытия заявки', options=self.close_author(), value=self.__existed_data[4])
        self.__data[5] = Dropdown(hint_text='Пациент', options=self.close_author(), value=self.__existed_data[5])
        self.__data[6] = Dropdown(hint_text='МКБ', options=self.mkb(), value=self.__existed_data[6])
        self.__data[7] = Dropdown(hint_text='Услуга', options=self.service(), value=self.__existed_data[7])
        self.__data[8] = TextField(label="Хронические заболевания", value=self.__existed_data[8])
        self.__data[9] = TextField(label="Комментарий при оформлении", value=self.__existed_data[9])
        self.__data[10] = TextField(label="Комментарий", value=self.__existed_data[10])
        self.__data[11] = TextField(label="Стоимость", value=self.__existed_data[12], input_filter=NumbersOnlyInputFilter())
        self.__data[12] = Dropdown(hint_text='Автор заявки', options=self.close_author(), value=self.__existed_data[13])
        self.__data[13] = Dropdown(hint_text='Подтверждение факта поступления', options=self.hospitalized(), value=self.__existed_data[14])
        self.__data[14] = Dropdown(hint_text='Клиника', options=self.hospital(), value=self.__existed_data[15])
        self.__data[15] = TextField(label="Вознаграждение", value=self.__existed_data[16], suffix_text="В формате: 9.99 (не >9.99)")
        self.__data[16] = Dropdown(hint_text='Статус вознаграждения', options=self.benefit_status(), value=self.__existed_data[17])
        self.__data[17] = TextField(label="Дата создания", value=self.__existed_data[18], suffix_text="В формате: дд-мм-гг")
        self.__data[18] = TextField(label="Дата уведомления", value=self.__existed_data[19], suffix_text="В формате: дд-мм-гг")
        self.__data[19] = TextField(label="Дата госпитализации", value=self.__existed_data[20], suffix_text="В формате: дд-мм-гг")
        self.__data[20] = TextField(label="Дата закрытия заявки", value=self.__existed_data[21], suffix_text="В формате: дд-мм-гг")
        self.__data[21] = FilledButton(text='Сохранить', on_click=self.save_changes)
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
                        Divider(height=10),
                        Container(
                            Text(value='Болезнь', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[5], padding=padding.only(left=50, right=50)),
                        Container(self.__data[6], padding=padding.only(left=50, right=50)),
                        Container(self.__data[7], padding=padding.only(left=50, right=50)),
                        Container(self.__data[8], padding=padding.only(left=50, right=50)),
                        Container(self.__data[9], padding=padding.only(left=50, right=50)),
                        Container(self.__data[10], padding=padding.only(left=50, right=50)),
                        Divider(height=10),
                        Container(
                            Text(value='Финансы', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[11], padding=padding.only(left=50, right=50)),
                        Container(self.__data[12], padding=padding.only(left=50, right=50)),
                        Container(self.__data[13], padding=padding.only(left=50, right=50)),
                        Container(self.__data[14], padding=padding.only(left=50, right=50)),
                        Container(self.__data[15], padding=padding.only(left=50, right=50)),
                        Container(self.__data[16], padding=padding.only(left=50, right=50)),
                        Divider(height=10),
                        Container(
                            Text(value='Даты', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[17], padding=padding.only(left=50, right=50)),
                        Container(self.__data[18], padding=padding.only(left=50, right=50)),
                        Container(self.__data[19], padding=padding.only(left=50, right=50)),
                        Container(self.__data[20], padding=padding.only(left=50, right=50)),
                        Container(self.__data[21], padding=padding.only(left=50, right=50, top=10, bottom=10)),
                    ],
                    scroll=ScrollMode.ALWAYS,
                    )
                )
            )
        )


class change_applications:
    def __init__(self, vault, config, db):
        super(change_applications, self).__init__()
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_drop_box = LoadDropBox(db)
        self.__load_pages = LoadPages(db)
        self.__process_data = ProcessData()
        self.__states = None
        self.__save = None
        self.__reward = None
        self.__reward_status = None
        self.__date_of_creation = None
        self.__date_of_notifications = None
        self.__date_of_hospitalization = None
        self.__application_closing_date = None
        self.__clinic = None
        self.__confirmation_of_receipt = None
        self.__author_of_the_application = None
        self.__cost = None
        self.__comment_at_checkout = None
        self.__number = None
        self.__application_type = None
        self.__payment_type = None
        self.__application_status = None
        self.__author_of_closing_request = None
        self.__patient = None
        self.__mkb = None
        self.__service = None
        self.__comment = None
        self.__chronic_diseases = None
        self.__data_buttons = [self.__number, self.__application_type, self.__payment_type, self.__application_status,
                       self.__author_of_closing_request, self.__patient, self.__mkb, self.__service,
                       self.__chronic_diseases,
                       self.__comment_at_checkout, self.__comment, self.__cost, self.__author_of_the_application,
                       self.__confirmation_of_receipt, self.__clinic,
                       self.__reward, self.__reward_status, self.__date_of_creation, self.__date_of_notifications,
                       self.__date_of_hospitalization, self.__application_closing_date, self.__save]

    def change_application(self, pg: PageData):
        row_id = pg.page.client_storage.get("current_action")[1]
        self.__states = {'add': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data),
         'change': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data, self.__load_pages, row_id)}
        if row_id is not None:
            name = 'изменить'
        else:
            name = 'создать'
        pg.page.title = f"Заявки - {name}"
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
