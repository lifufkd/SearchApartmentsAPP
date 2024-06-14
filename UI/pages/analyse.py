#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import PageData
from modules.CRUD import CRUD
############static variables#####################

#################################################


class Analyse:
    def __init__(self, db):
        super(Analyse, self).__init__()
        self.__crud = CRUD(db)

    def analyse(self, pg: PageData):
        pass