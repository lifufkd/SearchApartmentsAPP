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
from modules.utilites import insert_data_users, update_data_users


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
        data = self.__process_data.users(self.__data)
        if self.__row_id is None:
            try:
                insert_data_users(self.__db, 'users', data)
                self.init_dlg(True)
            except:
                self.init_dlg(False)
        else:
            try:
                update_data_users(self.__db, 'users', data, self.__row_id)
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

    def region(self):
        carts = list()
        for cart in self.__load_drop_box.region():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def role(self):
        carts = list()
        roles = [['Администратор', 0], ['Модератор', 1], ['Куратор', 2], ['Пользователь', 3], ['Не определена', 4]]
        for cart in roles:
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def area(self):
        carts = list()
        for cart in self.__load_drop_box.area():
            carts.append(
                dropdown.Option(text=cart[0], key=cart[1])
            )
        return carts

    def existed_data(self):
        return self.__load_pages.users(self.__row_id)

    def build(self):
        if self.__row_id is not None:
            self.__existed_data = self.existed_data()
        else:
            for x in range(14):
                if x in [9, 10]:
                    self.__existed_data.append(False)
                else:
                    self.__existed_data.append('')
        self.__data[0] = Dropdown(hint_text='Роль', options=self.role(), value=self.__existed_data[0])
        self.__data[1] = TextField(label="Имя", value=self.__existed_data[1])
        self.__data[2] = TextField(label="Фамилия", value=self.__existed_data[2])
        self.__data[3] = TextField(label="Отчество", value=self.__existed_data[3])
        self.__data[4] = TextField(label="День рождения", value=self.__existed_data[4], suffix_text="В формате дд-мм-гг")
        self.__data[5] = TextField(label="E-mail", value=self.__existed_data[5])
        self.__data[6] = TextField(label="Телефон", value=self.__existed_data[6], prefix_text="+7", input_filter=NumbersOnlyInputFilter())
        self.__data[7] = Dropdown(hint_text='Регион', options=self.region(), value=self.__existed_data[7])
        self.__data[8] = Dropdown(hint_text='Область', options=self.area(), value=self.__existed_data[8])
        self.__data[9] = Switch(value=self.__existed_data[9])
        self.__data[10] = Switch(value=self.__existed_data[10])
        self.__data[11] = TextField(label='Пароль', password=True, can_reveal_password=True, value=self.__existed_data[11])
        self.__data[12] = TextField(label='Повторите пароль', password=True, can_reveal_password=True, value=self.__existed_data[11])
        self.__data[13] = FilledButton(text='Сохранить', on_click=self.save_changes)
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
                            Text(value='Основная информация', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[0], padding=padding.only(left=50, right=50)),
                        Container(self.__data[1], padding=padding.only(left=50, right=50)),
                        Container(self.__data[2], padding=padding.only(left=50, right=50)),
                        Container(self.__data[3], padding=padding.only(left=50, right=50)),
                        Container(self.__data[4], padding=padding.only(left=50, right=50)),
                        Container(self.__data[5], padding=padding.only(left=50, right=50)),
                        Container(self.__data[6], padding=padding.only(left=50, right=50)),
                        Container(self.__data[7], padding=padding.only(left=50, right=50)),
                        Container(self.__data[8], padding=padding.only(left=50, right=50)),
                        Container(Text(value='Агент', size=14), padding=padding.only(left=50, right=50, top=7)),
                        Container(self.__data[9], padding=padding.only(left=50, right=50)),
                        Container(Text(value='Заблокирован', size=14), padding=padding.only(left=50, right=50, top=7)),
                        Container(self.__data[10], padding=padding.only(left=50, right=50)),
                        Divider(height=5),
                        Container(
                            Text(value='Изменить пароль', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[11], padding=padding.only(left=50, right=50)),
                        Container(self.__data[12], padding=padding.only(left=50, right=50)),
                        Container(self.__data[13], padding=padding.only(left=50, right=50, top=10, bottom=10))
                    ],
                        scroll=ScrollMode.ALWAYS,
                    )
                )
            )
        )

class change_users:
    def __init__(self, vault, config, db):
        super(change_users, self).__init__()
        self.__save = None
        self.__password_retry = None
        self.__password = None
        self.__blocked = None
        self.__agent = None
        self.__area = None
        self.__region = None
        self.__phone = None
        self.__email = None
        self.__birthday = None
        self.__last_name = None
        self.__middle_name = None
        self.__name = None
        self.__role = None
        self.__states = None
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_drop_box = LoadDropBox(db)
        self.__load_pages = LoadPages(db)
        self.__process_data = ProcessData()
        self.__data_buttons = [self.__role, self.__name, self.__middle_name, self.__last_name, self.__birthday,
                               self.__email, self.__phone, self.__region, self.__area, self.__agent, self.__blocked,
                               self.__password, self.__password_retry, self.__save]

    def change_users(self, pg: PageData):
        row_id = pg.page.client_storage.get("current_action")[1]
        self.__states = {'add': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data),
                         'change': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db,
                                           self.__process_data, self.__load_pages, row_id)}
        if row_id is not None:
            name = 'изменить'
        else:
            name = 'создать'
        pg.page.title = f"Пользователи - {name}"
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
