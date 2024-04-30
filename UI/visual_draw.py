#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import flet as ft
from flet_navigator import VirtualFletNavigator
from UI.pages import log_in, main, applications, clinics, profile, ksg, ratio, mkb, region, area, med_profile, users, service
from UI.pages.change import change_users, change_mkb, change_med_profile, change_ksg, change_clinics, change_area, change_applications, change_service
############static variables#####################

#################################################


class UI:
    def __init__(self, config, db):
        super(UI, self).__init__()
        self.__vault_keys = ['current_user']
        self.__config = config
        self.__db = db
        self.__log_in = log_in.Log_in(self.__vault_keys, config, db)
        self.__main = main.Main(self.__vault_keys, config, db)
        self.__application = applications.Application(self.__vault_keys, config, db)
        self.__clinic = clinics.Clinic(self.__vault_keys, config, db)
        self.__profile = profile.Profile(self.__vault_keys, config, db)
        self.__ksg = ksg.Ksg(self.__vault_keys, config, db)
        self.__mkb = mkb.Mkb(self.__vault_keys, config, db)
        self.__ratio = ratio.Ratio(self.__vault_keys, config, db)
        self.__region = region.Region(self.__vault_keys, config, db)
        self.__area = area.Area(self.__vault_keys, config, db)
        self.__med_profile = med_profile.Med_profile(self.__vault_keys, config, db)
        self.__users = users.User(self.__vault_keys, config, db)
        self.__service = service.Service(self.__vault_keys, config, db)
        self.__change_clinics = change_clinics.change_clinics(self.__vault_keys, config, db)
        self.__change_applications = change_applications.change_applications(self.__vault_keys, config, db)
        self.__change_users = change_users.change_users(self.__vault_keys, config, db)
        self.__change_ksg = change_ksg.change_ksg(self.__vault_keys, config, db)
        self.__change_mkb = change_mkb.change_mkb(self.__vault_keys, config, db)
        self.__change_med_profile = change_med_profile.change_med_profile(self.__vault_keys, config, db)
        self.__change_area = change_area.change_area(self.__vault_keys, config, db)
        self.__change_service = change_service.change_service(self.__vault_keys, config, db)

    def main(self, page: ft.Page):
        page.theme_mode = 'dark'
        flet_navigator = VirtualFletNavigator(
            {
                '/': self.__log_in.log_in,
                'main': self.__main.main,
                'application': self.__application.application,
                'clinic': self.__clinic.clinic,
                'profile': self.__profile.profile,
                'ratio': self.__ratio.ratio,
                'ksg': self.__ksg.ksg,
                'mkb': self.__mkb.mkb,
                'region': self.__region.region,
                'area': self.__area.area,
                'med_profile': self.__med_profile.med_profile,
                'service': self.__service.service,
                'user': self.__users.user,
                'applications_change_applications': self.__change_applications.change_application,
                'clinics_change_clinics': self.__change_clinics.change_clinics,
                'users_change_users': self.__change_users.change_users,
                'ksg_change_ksg': self.__change_ksg.change_ksg,
                'mkb_change_mkb': self.__change_mkb.change_mkb,
                'med_profile_change_med_profile': self.__change_med_profile.change_med_profile,
                'area_change_area': self.__change_area.change_area,
                'service_change_service': self.__change_service.change_service,
            }
        )
        flet_navigator.render(page)

