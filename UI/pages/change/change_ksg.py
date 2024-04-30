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
from modules.utilites import insert_data_ksg, update_data_ksg


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
        data = self.__process_data.ksg(self.__data)
        if self.__row_id is None:
            try:
                insert_data_ksg(self.__db, data)
                self.init_dlg(True)
            except Exception as e:
                print(e)
                self.init_dlg(False)
        else:
            try:
                update_data_ksg(self.__db, data, self.__row_id)
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
        return self.__load_pages.ksg(self.__row_id)

    def build(self):
        if self.__row_id is not None:
            self.__existed_data = self.existed_data()
        else:
            for x in range(12):
                self.__existed_data.append('')
        self.__data[0] = TextField(label="Код", value=self.__existed_data[0])
        self.__data[1] = TextField(label="Название", value=self.__existed_data[1])
        self.__data[2] = TextField(label="Стоимость", value=self.__existed_data[2])
        self.__data[3] = TextField(label="Коэффициент затрат", value=self.__existed_data[3])
        self.__data[4] = TextField(label="Коэффициенты специфики", value=self.__existed_data[4])
        self.__data[5] = TextField(label="Коэффициент уровня", value=self.__existed_data[5])
        self.__data[6] = TextField(label="Доля зарплаты и прочих расходов", value=self.__existed_data[6])
        self.__data[7] = Switch(value=self.__existed_data[7])
        self.__data[8] = TextField(label="МКБ", value=self.__existed_data[8])
        self.__data[9] = TextField(label="Услуги", value=self.__existed_data[9])
        self.__data[10] = TextField(label="Мед. профили", value=self.__existed_data[10])
        self.__data[11] = FilledButton(text='Сохранить', on_click=self.save_changes)
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
                            Text(value='Информация о КСГ', size=20),
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
                        Divider(height=10),
                        Container(
                            Text(value='Коэффициенты', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[3], padding=padding.only(left=50, right=50)),
                        Container(self.__data[4], padding=padding.only(left=50, right=50)),
                        Container(self.__data[5], padding=padding.only(left=50, right=50)),
                        Container(self.__data[6], padding=padding.only(left=50, right=50)),
                        Container(
                            Text(value='Коэффициент уровня мед учреждения', size=14),
                            padding=padding.only(left=50, right=50, top=5,),
                        ),
                        Container(self.__data[7], padding=padding.only(left=50, right=50)),
                        Divider(height=10),
                        Container(
                            Text(value='Связи', size=20),
                            padding=padding.only(left=50, right=50, top=15, bottom=7),
                        ),
                        Container(self.__data[8], padding=padding.only(left=50, right=50)),
                        Container(self.__data[9], padding=padding.only(left=50, right=50)),
                        Container(self.__data[10], padding=padding.only(left=50, right=50)),
                        Container(self.__data[11], padding=padding.only(left=50, right=50, top=10, bottom=10)),
                    ],
                        scroll=ScrollMode.ALWAYS,
                    )
                )
            )
        )

class change_ksg:
    def __init__(self, vault, config, db):
        super(change_ksg, self).__init__()
        self.__save = None
        self.__med_profiles = None
        self.__service = None
        self.__mkb = None
        self.__coefficient_of_the_medical_institution_level = None
        self.__share_of_salary_and_other_expenses = None
        self.__level_coefficient = None
        self.__specificity_coefficients = None
        self.__cost_ratio = None
        self.__cost = None
        self.__name = None
        self.__code = None
        self.__states = None
        self.__vault = vault
        self.__config = config
        self.__db = db
        self.__load_drop_box = LoadDropBox(db)
        self.__load_pages = LoadPages(db)
        self.__process_data = ProcessData()
        self.__data_buttons = [self.__code, self.__name, self.__cost, self.__cost_ratio,
                               self.__specificity_coefficients,
                               self.__level_coefficient, self.__share_of_salary_and_other_expenses,
                               self.__coefficient_of_the_medical_institution_level, self.__mkb, self.__service,
                               self.__med_profiles, self.__save]

    def change_ksg(self, pg: PageData):
        row_id = pg.page.client_storage.get("current_action")[1]
        self.__states = {'add': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db, self.__process_data),
                         'change': Content(self.__load_drop_box, self.__data_buttons, pg, self.__db,
                                           self.__process_data, self.__load_pages, row_id)}
        if row_id is not None:
            name = 'изменить'
        else:
            name = 'создать'
        pg.page.title = f"КСГ - {name}"
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