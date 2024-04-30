#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
#################################################


class SideBar(UserControl):
    def __init__(self, vault, pg):
        super().__init__()
        self.__buttonnames = ['Главная', 'Заявки', 'Клиники', 'Пользователи', 'Услуги', 'КСГ', 'МКБ', 'Базовая ставка', 'Регионы', 'Области', 'Мед. профили', 'Выйти', 'Пользователь']
        self.__vault = vault
        self.__pg = pg
        self.__user_info = pg.page.session.get(self.__vault[0])

    def navigation(self, e): #настроки для навигации
        if self.__buttonnames[0] == e.control.tooltip:
            self.__pg.navigator.navigate('main', self.__pg.page)
        elif self.__buttonnames[1] == e.control.tooltip:
            self.__pg.navigator.navigate('application', self.__pg.page)
        elif self.__buttonnames[2] == e.control.tooltip:
            self.__pg.navigator.navigate('clinic', self.__pg.page)
        elif self.__buttonnames[3] == e.control.tooltip:
            self.__pg.navigator.navigate('user', self.__pg.page)
        elif self.__buttonnames[4] == e.control.tooltip:
            self.__pg.navigator.navigate('service', self.__pg.page)
        elif self.__buttonnames[5] == e.control.tooltip:
            self.__pg.navigator.navigate('ksg', self.__pg.page)
        elif self.__buttonnames[6] == e.control.tooltip:
            self.__pg.navigator.navigate('mkb', self.__pg.page)
        #elif self.__buttonnames[7] == e.control.tooltip:
            #self.__pg.navigator.navigate('ratio', self.__pg.page)
        elif self.__buttonnames[8] == e.control.tooltip:
            self.__pg.navigator.navigate('region', self.__pg.page)
        elif self.__buttonnames[9] == e.control.tooltip:
            self.__pg.navigator.navigate('area', self.__pg.page)
        elif self.__buttonnames[10] == e.control.tooltip:
            self.__pg.navigator.navigate('med_profile', self.__pg.page)
        elif self.__buttonnames[11] == e.control.tooltip:
            self.__pg.navigator.navigate('/', self.__pg.page)
            self.__pg.page.session.remove(self.__vault[0])
        elif self.__buttonnames[12] == e.control.tooltip:
            self.__pg.navigator.navigate('profile', self.__pg.page)

    def HighLight(self, e):
        # хуйня чтобы подсвечивались кнопки в сайдбаре
        if e.data == 'true':
            e.control.bgcolor = 'white10'
            e.control.update()
        else:
            e.control.bgcolor = None
            e.control.update()
            e.control.content.controls[0].icon_color = "white54"
            e.control.content.controls[1].color = "white54"
            e.control.update()

    def UserData(self, initials: str, name: str, descriptions: str):
        return Container(
            on_click=lambda e: self.navigation(e),
            tooltip='Пользователь',
            content=Row(
                controls=[
                    Container(  # это квадрат с инициалами
                        width=42,
                        height=42,
                        bgcolor='bluegrey900',
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            value=initials,
                            size=22,
                            weight="bold",
                        ),
                    ),
                    Column(
                        spacing=1,
                        alignment='center',
                        controls=[
                            Text(  # текст с именем и фамилией
                                value=name,
                                size=15,
                                weight='bold',
                                opacity=1,
                                animate_opacity=200  # скорость анимации
                            ),
                            Text(
                                value=descriptions, #Frontend dev
                                size=12,
                                weight='w400',
                                color="white54",
                                opacity=1,
                                animate_opacity=200,  # скорость анимации
                            )
                        ]
                    )
                ]
            )
        )

    def ContainedIcon(self, icon_name: str, text: str):
        return Container(
            width=180,
            height=45,
            border_radius=10,
            on_hover=lambda e: self.HighLight(e),
            on_click=lambda e: self.navigation(e),
            tooltip=text,
            content=Row(
                controls=[
                    IconButton(
                        icon=icon_name,
                        icon_size=18,
                        icon_color='white54',
                        style=ButtonStyle(
                            shape={
                                "": RoundedRectangleBorder(radius=7),
                            },
                            overlay_color={"": "transparent"},
                        ),
                    ),
                    Text(
                        value=text,
                        color="white54",
                        size=15,
                        opacity=1,
                        animate_opacity=200,
                    )
                ]

            )
        )

    def build(self):
        return Container(
            padding=30,
            content=Column(
                controls=[
                    # сюда иконки хуярить, будут в столбик
                    self.UserData(f'{self.__user_info[1][0][0].upper()}{self.__user_info[1][1][0].upper()}', f'{self.__user_info[1][0]} {self.__user_info[1][1]}', self.__user_info[2]),  # инициалы челов
                    Divider(height=5),
                    self.ContainedIcon(icons.HOUSE, self.__buttonnames[0]),
                    self.ContainedIcon(icons.REQUEST_PAGE, self.__buttonnames[1]),
                    self.ContainedIcon(icons.BUSINESS_OUTLINED, self.__buttonnames[2]),
                    self.ContainedIcon(icons.SUPERVISED_USER_CIRCLE, self.__buttonnames[3]),
                    Divider(height=5),
                    self.ContainedIcon(icons.MEDICAL_SERVICES_OUTLINED, self.__buttonnames[5]),
                    self.ContainedIcon(icons.MEDICAL_SERVICES_OUTLINED, self.__buttonnames[6]),
                    self.ContainedIcon(icons.ATTACH_MONEY, self.__buttonnames[4]),
                    #self.ContainedIcon(icons.ATM_ROUNDED, self.__buttonnames[7]),
                    Divider(height=5),
                    self.ContainedIcon(icons.AREA_CHART_OUTLINED, self.__buttonnames[8]),
                    self.ContainedIcon(icons.AREA_CHART, self.__buttonnames[9]),
                    self.ContainedIcon(icons.MEDICATION_LIQUID_SHARP, self.__buttonnames[10]),
                    Divider(height=5),
                    self.ContainedIcon(icons.LOGOUT_ROUNDED, self.__buttonnames[11]),
                ],
            ),
        )