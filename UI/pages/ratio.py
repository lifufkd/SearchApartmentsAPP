#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from flet import *
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from flet_navigator import PageData
from UI.sidebar import SideBar
#################################################


class Ratio:
    def __init__(self, vault, config, db):
        super(Ratio, self).__init__()
        self.__vault = vault
        self.__config = config

    def ratio(self, pg: PageData):
        pg.page.title = "Базовая ставка"
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
                ],
                expand=True,
            )
        )
        pg.page.update()
        plt.close()