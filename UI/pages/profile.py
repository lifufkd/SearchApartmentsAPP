#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
from flet_navigator import PageData
from UI.sidebar import SideBar
from modules.utilites import update_profile


#################################################


class ChangeProfile(UserControl):
    def __init__(self, pg, db, vault):
        super().__init__()
        self.__dlg_modal = None
        self.__last_name = None
        self.__middle_name = None
        self.__user_name = None
        self.__user_pass = None
        self.__user_pass_confirm = None
        self.__user_login = None
        self.__btn_save = None
        self.__pg = pg
        self.__db = db
        self.__vault = vault
        self.__user_info = pg.page.session.get(self.__vault[0])
        print(self.__user_info)

    def savechanges(self, event):
        if self.__user_pass.value == self.__user_pass_confirm.value:
            self.__pg.page.session.set(self.__vault[0], update_profile([self.__user_login.value, [self.__user_name.value, self.__middle_name.value, self.__last_name.value], self.__user_pass.value], self.__user_info, self.__db))
            self.dlg_modal(['Данные успешно сохранены!', 'god damn right'])
            self.open_dlg_modal(None)
        else:
            self.dlg_modal(['Введенные пароли не совпадают', 'Повторите попытку'])
            self.open_dlg_modal(None)

    def close_dlg(self, e):
        self.__dlg_modal.open = False
        self.__pg.page.update()

    def open_dlg_modal(self, e):
        self.__pg.page.dialog = self.__dlg_modal
        self.__dlg_modal.open = True
        self.__pg.page.update()

    def validate(self, event):
        if (self.__user_name.value + self.__user_pass.value + self.__user_pass_confirm.value + self.__user_login.value + self.__middle_name.value + self.__last_name.value) != '':
            self.__btn_save.disabled = False
        else:
            self.__btn_save.disabled = True
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

    def build(self):
        #ЗНАЧЕНИЯ#
        self.__user_name = TextField(label='Фамилия', on_change=self.validate)
        self.__middle_name = TextField(label='Имя', on_change=self.validate)
        self.__last_name = TextField(label='Отчество', on_change=self.validate)
        self.__user_pass = TextField(label='Пароль', password=True, on_change=self.validate, can_reveal_password=True)
        self.__user_pass_confirm = TextField(label='Подтвердите пароль', password=True, on_change=self.validate, can_reveal_password=True)
        self.__user_login = TextField(label='Логин', on_change=self.validate)
        self.__btn_save = OutlinedButton(text='Сохранить', width=200, on_click=self.savechanges)

        return Container(
            height=1500,
            content=Column(
                [
                    Container(
                        content=Text(value='Профиль', size=20),
                        padding=padding.only(left=60, right=60, top=20)
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__user_name
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__middle_name
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__last_name
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__user_login
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__user_pass
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__user_pass_confirm
                    ),
                    Container(
                        padding=padding.only(left=60, right=60),
                        content=self.__btn_save,
                    ),
                ],
                expand=True,
                alignment=MainAxisAlignment.START,
            ),
        )


class Profile:
    def __init__(self, vault, config, db):
        super(Profile, self).__init__()
        self.__vault = vault
        self.__config = config
        self.__db = db

    def profile(self, pg: PageData):
        pg.page.title = "Профиль"
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
                        content=ChangeProfile(pg, self.__db, self.__vault),
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