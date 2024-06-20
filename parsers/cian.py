#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import cianparser
import random
from datetime import datetime, timedelta
from modules.CRUD import CRUD

############static variables#####################
#################################################


def get_date():
    # Вычисление разницы между двумя датами в секундах
    start_date = datetime.today() - timedelta(days=365)
    end_date = datetime.today() + timedelta(days=365)
    delta = end_date - start_date
    int_delta = int(delta.total_seconds())
    second = random.randint(0, int_delta)
    date = start_date + timedelta(seconds=second)
    return date.strftime("%Y-%m-%d %H:%M")


class Cian:
    def __init__(self, db, config, type):
        super(Cian, self).__init__()
        self.__crud = CRUD(db)
        self.__config = config
        self.__type = type
        self.__current_parameters = None
        self.__parameters = [
            [
                "price"
            ],
            [
                "price_per_month"
            ],
            [
                "price"
            ]
        ]
        # запускаем парсер init()
        self.init()

    def flats_parse(self, data):
        for i in data:
            temp = list()
            if self.__crud.get_existed_apartment(i['url']):
                address = f"{i['location']}, {i['street']}, {i['house_number']}"
                floor = f'{i["floor"]} из {i["floors_count"]}'
                date = get_date()
                temp.extend([i['url'], address, floor, i['total_meters'], i['rooms_count'], i[self.__current_parameters[0]], date, 'Циан'])
                # Проверяем отсутствие ошибки
                if len(set(temp)) > 3:
                    self.__crud.add_apartment(temp, self.__type)
            else:
                return False
        return True

    def house_parser(self, data):
        for i in data:
            temp = list()
            if self.__crud.get_existed_apartment(i['url']):
                address = f"{i['location']}, {i['street']}, {i['house_number']}"
                date = get_date()
                temp.extend([i['url'], address, 0, random.randint(45, 300), random.randint(1, 8), i[self.__current_parameters[0]], date, 'Циан'])
                # Проверяем отсутствие ошибки
                if len(set(temp)) > 3:
                    self.__crud.add_apartment(temp, self.__type)
            else:
                return False
        return True

    def init(self):
        deal_type = None
        flag = None
        match self.__type:
            case "Купить":
                self.__current_parameters = self.__parameters[0]
                flag = True
                deal_type = "sale"
            case "Снять":
                self.__current_parameters = self.__parameters[1]
                flag = True
                deal_type = "rent_long"
            case "Загородное_жильё":
                self.__current_parameters = self.__parameters[2]
                flag = False
                deal_type = "sale"
        while True:
            if self.__crud.get_all_count_apartments() >= self.__config.get_config()['parse_limit']:
                break
            for i in cianparser.list_locations():
                counter = 1
                while True:
                    if self.__crud.get_all_count_apartments() >= self.__config.get_config()['parse_limit']:
                        break
                    parser = cianparser.CianParser(location=i[0])
                    if flag:
                        data = parser.get_flats(rooms="all", deal_type=deal_type,
                                                       additional_settings={"start_page": counter, "end_page": counter})
                    else:
                        data = parser.get_suburban(suburban_type="townhouse", deal_type=deal_type,
                                                       additional_settings={"start_page": counter, "end_page": counter})
                    if flag:
                        data = self.flats_parse(data)
                    else:
                        data = self.house_parser(data)
                    if data:
                        break
                    else:
                        counter += 1