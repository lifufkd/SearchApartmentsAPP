#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import threading
import time
from seleniumbase import Driver
from datetime import datetime
from selenium.webdriver.common.by import By
from modules.CRUD import CRUD

############static variables#####################
#################################################


class Avito:
    def __init__(self, db, config, type):
        super(Avito, self).__init__()
        self.__driver = None
        self.__crud = CRUD(db)
        self.__config = config
        self.__paths = None
        self.__type = type
        self.__threads_drivers = list()
        self.__months = {
                        1: "Января",
                        2: "Февраля",
                        3: "Марта",
                        4: "Апреля",
                        5: "Мая",
                        6: "Июня",
                        7: "Июля",
                        8: "Августа",
                        9: "Сентября",
                        10: "Октября",
                        11: "Ноября",
                        12: "Декабря"
                    }
        self.__appartaments_type = [
            [
                "https://www.avito.ru/all/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA",
                "iva-item-body-KLUuy",
                'div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > span',
                'params-paramsList-_awNW',
                'div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div > div > div > div > div > div > div > span > span > span',
                'style-item-footer-text-LEjEe',
                "Купить"
            ],
            [
                "https://www.avito.ru/all/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA",
                "iva-item-content-rejJg",
                "div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > span",
                "params-paramsList-_awNW",
                "div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div > div > div > div > div > div > div > span > span > span",
                "style-item-footer-text-LEjEe",
                "Снять"

            ],
            [
                "https://www.avito.ru/all/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA",
                "iva-item-content-rejJg",
                "div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > span",
                "params-paramsList-_awNW",
                "div#app > div > div:nth-of-type(6) > div > div > div:nth-of-type(2) > div:nth-of-type(3) > div:nth-of-type(2) > div > div > div > div > div > div > div > div > div > span > span > span",
                "style-item-footer-text-LEjEe",
                "Загородное_жильё"
            ]
        ]
        #запускаем парсер init()
        self.init()

    #проверка освобождения потоков
    def queue_checker(self, threads):
        while True:
            c = 0
            for thread in threads:
                if not thread.is_alive():
                    c += 1
            if c == len(threads):
                break
            time.sleep(0.5)

    def init(self):
        #создаём объект хром драйвера
        self.__driver = Driver(ad_block_on=True, uc=True)
        # заранее создаём объекты браузеров для потоков
        for i in range(self.__config.get_config()['threads_count']):
            self.__threads_drivers.append(Driver(ad_block_on=True, uc=True))
        match self.__type:
            case "Купить":
                self.__paths = self.__appartaments_type[0]
            case "Снять":
                self.__paths = self.__appartaments_type[1]
            case "Загородное_жильё":
                self.__paths = self.__appartaments_type[2]
        self.links_parser()

    def page_parse(self, link, driver_index):
        data = [link]
        #создаём копии хрома для асинхронного парсинга данных о квартирах
        driver_page = self.__threads_drivers[driver_index]
        driver_page.get(link)
        time.sleep(3)
        for index, i in enumerate(self.__paths[2:-1]):
            try:
                if index == 1:
                    page_data = driver_page.find_element(By.CLASS_NAME, i).text
                elif index == 3:
                    page_data = driver_page.find_element(By.CLASS_NAME, i).find_elements(By.TAG_NAME, 'span')[1].text
                elif index == 0:
                    page_data = driver_page.find_element(By.CSS_SELECTOR, i).text
                elif index == 2:
                    page_data = driver_page.find_element(By.CSS_SELECTOR, i).text
            except Exception as e:
                print(index)
                print(e)
                if index == 1:
                    for k in range(3):
                        data.append('-')
                else:
                    data.append('-')
                continue
            match index:
                case 0:
                    # парсим адрес
                    data.append(page_data.split('\n')[0])
                case 1:
                    # парсим этаж, площадь, количество комнат
                    page_data_array = page_data.split('\n')
                    for g in ['Этаж', 'Общая площадь', 'Количество комнат']:
                        flag = False
                        for search in page_data_array:
                            if g in search:
                                flag = True
                                data.append(search[len(g)+2:])
                        if not flag:
                            data.append('-')
                case 2:
                    # парсим цену
                    data.append(page_data.split('\n')[0])
                case 3:
                    # парсим дату публикации
                    if 'сегодня' in page_data or 'вчера' in page_data:
                        current_date = datetime.now()
                        # Форматируем дату в требуемом формате
                        formatted_date = "{:02d} {}".format(current_date.day, self.__months[current_date.month])
                        v_index = page_data.find(' в ')
                        data.append(f'{formatted_date} {page_data[v_index+1:]}')
                    else:
                        data.append(page_data[2:])
        data.append('Авито')
        print(data)
        # Проверяем отсутствие ошибки
        if len(set(data)) > 3:
            self.__crud.add_apartment(data, self.__paths[-1])

    def links_parser(self):
        c = 1
        while True:
            if self.__crud.get_all_count_apartments() >= self.__config.get_config()['parse_limit']:
                break
            index = 0
            threads = list()
            self.__driver.get(
                f'{self.__paths[0]}&p={c}')
            cards = self.__driver.find_elements(By.CLASS_NAME, self.__paths[1])
            links_app = list()
            for i in cards:
                links = i.find_elements(By.TAG_NAME, 'a')
                links_app.append(links[0].get_attribute('href'))
            print(links_app)
            while True:
                if len(links_app[index:]) > self.__config.get_config()['threads_count']:
                    for link in range(self.__config.get_config()['threads_count']):
                        #создаём задачу для асинхронного парсинга каждой страницы с квартирой
                        if self.__crud.get_existed_apartment(links_app[index+link]):
                            task = threading.Thread(target=self.page_parse, args=(links_app[index+link], link))
                            task.start()
                            threads.append(task)
                    self.queue_checker(threads)
                    index += self.__config.get_config()['threads_count']
                elif 0 < len(links_app[index:]) <= self.__config.get_config()['threads_count']:
                    for link in range(len(links_app[index:])):
                        # создаём задачу для асинхронного парсинга каждой страницы с квартирой
                        if self.__crud.get_existed_apartment(links_app[index+link]):
                            task = threading.Thread(target=self.page_parse, args=(links_app[index + link], link))
                            task.start()
                            threads.append(task)
                    self.queue_checker(threads)
                    index += len(links_app[index:])
                else:
                    break
            c += 1

    #при завершении работы парсера производим закрытие браузеров и очистку памяти
    def __del__(self):
        self.__driver.quit()
        for i in self.__threads_drivers:
            i.quit()
