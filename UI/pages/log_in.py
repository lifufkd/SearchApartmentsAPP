#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import PageData
from modules.utilites import unparse_json
#################################################


class Log_in:
    def __init__(self, vault, config, db):
        super(Log_in, self).__init__()
        self.__vault = vault
        self.__config = config
        self.__db = db

    def log_in(self, pg: PageData):
        pg.page.title = "Вход"
        pg.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        images = ft.Row()
        for i in range(1):
            images.controls.append(
                ft.Image(
                    src=f'{self.__config["logo_path"]}',
                    width=420,
                )
            )
        pg.page.update()

        def close_dlg(e):
            dlg_modal.open = False
            pg.page.update()

        def open_dlg_modal(e):
            pg.page.dialog = dlg_modal
            dlg_modal.open = True
            pg.page.update()

        def login(event):
            user_data = self.__db.authorization(user_login.value, user_pass.value)
            if user_data is not None:
                user_data[1] = unparse_json(user_data[1])
                pg.page.session.set(self.__vault[0], user_data)
                pg.navigator.navigate('main', pg.page)
            else:
                open_dlg_modal(None)

        def validate(event):
            if all([user_login.value, user_pass.value]):
                btn_login.disabled = False
            else:
                btn_login.disabled = True
            pg.page.update()

        user_login = ft.TextField(label='Логин', width=400, on_change=validate)
        user_pass = ft.TextField(label='Пароль', width=400, on_change=validate, password=True, can_reveal_password=True)
        btn_login = ft.OutlinedButton(text='Войти', width=400, on_click=login, disabled=True)
        btn_save = ft.Checkbox(label='Запомнить', value=False)
        title_text = ft.Text(value='Добро пожаловать в SherDOC -\nздоровье это элементарно!',
                             text_align=ft.TextAlign.CENTER, size=20)
        under_text = ft.Text(value='Пожалуйста, войдите в свою учетную запись', size=15, text_align=ft.TextAlign.CENTER,
                             color='grey')
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Вы ввели неверные данные"),
            content=ft.Text("Повторите попытку"),
            actions=[
                ft.TextButton("Ok", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        pg.page.add(
            ft.Row(
                [
                    images
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            title_text
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    under_text
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            user_login,
                            user_pass,
                            btn_login,
                            btn_save
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
