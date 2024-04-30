#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
from modules.utilites import word_wrap, unparse_json


#################################################


class LoadData:
    def __init__(self, db):
        super(LoadData, self).__init__()
        self.__db = db
        # ограничение на количество элементов на одной странице (имплементация многостраничности)# DESC LIMIT 15 OFFSET {(c_page - 1) * 15}

    def application(self):
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 30  # перенос слов по 15 символов
        data = list()
        pointer = {1: 'application_type', 2: 'payment_type', 3: 'application_status', 4: 'hospitalized',
                   5: 'benefit_status', 6: 'date_format'}
        raw_data = self.__db.get_data(
            f'SELECT number, application_type, payment_type, application_status, hospitalized, status, date_create, id FROM application WHERE deleted = 0 ORDER BY date_create',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row in pointer.keys():
                    if row == 6:
                        if rows[row] is None:
                            l1.append('')
                        else:
                            l1.append(rows[row].strftime("%d-%m-%Y"))
                    else:
                        d = self.__db.get_data(f'SELECT title FROM {pointer[row]} WHERE id = "{rows[row]}" AND deleted = 0', ())
                        if len(d) > 0:
                            l1.append(word_wrap(
                                d[0][0],
                                max_len))
                        else:
                            l1.append('')
                elif row == 7:
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            data.append(l1)
        return data

    def area(self):
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 400  # перенос слов по 15 символов
        data = list()
        raw_data = self.__db.get_data(
            f'SELECT area, region, id FROM area WHERE deleted = 0 ORDER BY area',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row == 1:
                    d = self.__db.get_data(f'SELECT title FROM region WHERE id = "{rows[1]}" AND deleted = 0', ())
                    if len(d) > 0:
                        l1.append(d[0][0])
                    else:
                        l1.append('')
                elif row == 2:
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            data.append(l1)
        return data


    def clinics(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 30  # перенос слов по 15 символов
        raw_data = self.__db.get_data(
            f'SELECT name, med_profiles, site, phone_number, email, id FROM hospital WHERE deleted = 0 ORDER BY name',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row == 1:
                    profiles = ''
                    for item in unparse_json(rows[row]):
                        d = self.__db.get_data(f'SELECT med_profile FROM med_profile WHERE id = "{item}" AND deleted = 0', ())
                        if len(d) > 0:
                            profiles += d[0][0] + ', '
                        else:
                            l1.append('')
                    l1.append(word_wrap(profiles, max_len))
                elif row == 5:
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            data.append(l1)
        return data

    def ksg(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 30  # перенос слов по 15 символов
        pointer = {4: ['relative_ksg_mkb', 'id_ksg'], 5: ['relative_ksg_service', 'id_ksg'],
                   6: ['relative_ksg_med_profile', 'id_ksg']}
        raw_data = self.__db.get_data(
            f'SELECT code, title, price, ratio_switch, id FROM ksg WHERE deleted = 0 ORDER BY code',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows) + 2):
                if row == 3:
                    if rows[row] == 1:
                        l1.append(True)
                    else:
                        l1.append(False)
                elif row in pointer:
                    l1.append(self.__db.get_quantity(pointer[row][0], [pointer[row][1], rows[4]]))
                elif row == 2:
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            l1.append(rows[4])
            data.append(l1)
        return data

    def med_profile(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 400  # перенос слов по 15 символов
        pointer = {1: ['relative_ksg_med_profile', 'id_med_profile']}
        raw_data = self.__db.get_data(
            f'SELECT med_profile, id FROM med_profile WHERE deleted = 0 ORDER BY med_profile',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row in pointer:
                    l1.append(self.__db.get_quantity(pointer[row][0], [pointer[row][1], rows[1]]))
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            data.append(l1)
        return data

    def mkb(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 200  # перенос слов по 15 символов
        pointer = {2: ['relative_ksg_mkb', 'id_mkb'], 3: ['relative_mkb_service', 'id_mkb']}
        raw_data = self.__db.get_data(
            f'SELECT code, title, id FROM mkb WHERE deleted = 0 ORDER BY code',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows) + 1):
                if row in pointer:
                    l1.append(self.__db.get_quantity(pointer[row][0], [pointer[row][1], rows[2]]))
                else:
                    l1.append(word_wrap(rows[row], max_len))
            l1.append(rows[2])
            data.append(l1)
        return data

    def region(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 400  # перенос слов по 15 символов
        raw_data = self.__db.get_data(
            f'SELECT title, id FROM region WHERE deleted = 0 ORDER BY title',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row == 1:
                    l1.append(self.__db.get_quantity('area', ['region', rows[1]]))
                    l1.append(rows[row])
                else:
                    l1.append(word_wrap(rows[row], max_len))
            data.append(l1)
        return data

    def users(self):
        roles = {0: 'Администратор', 1: 'Модератор', 2: 'Куратор', 3: 'Пользователь', 4: 'Не определена', None: 'Не определена'}
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        raw_data = self.__db.get_data(
            f'SELECT id, role, full_name, photo, date_create, email, phone_number, agent, blocked FROM users WHERE deleted = 0 ORDER BY id',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows)):
                if row == 1:
                    l1.append(roles[rows[row]])
                elif row == 2:
                    fio = unparse_json(rows[row])
                    l1.append(f'{fio[0]}\n{fio[1]}\n{fio[2]}')
                elif row == 4:
                    if rows[row] is None:
                        l1.append('')
                    else:
                        l1.append(rows[row].strftime("%d-%m-%Y"))
                elif row in [7, 8]:
                    if rows[row] == 1:
                        l1.append(True)
                    else:
                        l1.append(False)
                else:
                    l1.append(rows[row])
            data.append(l1)
        return data

    def service(self):
        data = list()
        c_page = 1  # выбор страницы, в поле ввода по умолчанию поставить .value = 1
        max_len = 200  # перенос слов по 15 символов
        pointer = {2: ['relative_ksg_service', 'id_service'], 3: ['relative_mkb_service', 'id_service']}
        raw_data = self.__db.get_data(
            f'SELECT code, title, id FROM service WHERE deleted = 0 ORDER BY code',
            ())
        for rows in raw_data:
            l1 = []
            for row in range(len(rows) + 1):
                if row in pointer:
                    l1.append(self.__db.get_quantity(pointer[row][0], [pointer[row][1], rows[2]]))
                else:
                    l1.append(word_wrap(rows[row], max_len))
            l1.append(rows[2])
            data.append(l1)
        return data


class LoadDropBox:
    def __init__(self, db):
        super(LoadDropBox, self).__init__()
        self.__db = db

    def load_application_type(self):
        return self.__db.get_data(
            f'SELECT title, id FROM application_type WHERE deleted = 0 ORDER BY title',
            ())

    def load_payment_type(self):
        return self.__db.get_data(
            f'SELECT title, id FROM payment_type WHERE deleted = 0 ORDER BY title',
            ())

    def application_status(self):
        return self.__db.get_data(
            f'SELECT title, id FROM application_status WHERE deleted = 0 ORDER BY title',
            ())

    def close_author(self):
        return self.__db.get_data(
            f'SELECT full_name, id FROM users WHERE deleted = 0 ORDER BY full_name',
            ())

    def mkb(self):
        return self.__db.get_data(
            f'SELECT code, id FROM mkb WHERE deleted = 0 ORDER BY code',
            ())

    def service(self):
        return self.__db.get_data(
            f'SELECT code, id FROM service WHERE deleted = 0 ORDER BY code',
            ())

    def hospitalized(self):
        return self.__db.get_data(
            f'SELECT title, id FROM hospitalized WHERE deleted = 0 ORDER BY title',
            ())

    def hospital(self):
        return self.__db.get_data(
            f'SELECT name, id FROM hospital WHERE deleted = 0 ORDER BY name',
            ())

    def benefit_status(self):
        return self.__db.get_data(
            f'SELECT title, id FROM benefit_status WHERE deleted = 0 ORDER BY title',
            ())

    def region(self):
        return self.__db.get_data(
            f'SELECT title, id FROM region WHERE deleted = 0 ORDER BY title',
            ())

    def area(self):
        return self.__db.get_data(
            f'SELECT area, id FROM area WHERE deleted = 0 ORDER BY area',
            ())

    def ksg(self):
        return self.__db.get_data(
            f'SELECT code, id FROM ksg WHERE deleted = 0 ORDER BY code',
            ())

    def med_profile(self):
        return self.__db.get_data(
            f'SELECT med_profile, id FROM med_profile WHERE deleted = 0 ORDER BY med_profile',
            ())

    def base_ratio(self):
        return self.__db.get_data(
            f'SELECT parameter FROM ratio_settings WHERE deleted = 0 AND title = "ratio_diff"',
            ())

    def base_vote(self):
        return self.__db.get_data(
            f'SELECT parameter FROM ratio_settings WHERE deleted = 0 AND title = "base"',
            ())


class LoadPages:
    def __init__(self, db):
        super(LoadPages, self).__init__()
        self.__db = db

    def application(self, row_id):
        items = list()
        special_date = [18, 19, 20, 21]
        raw_data = self.__db.get_data(
            f'SELECT * FROM application WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0][1:])):
            if item in special_date:
                if raw_data[0][item+1] is None:
                    items.append('')
                else:
                    items.append(raw_data[0][item+1].strftime('%d-%m-%Y'))
            else:
                items.append(raw_data[0][item + 1])
        return items

    def area(self, row_id):
        items = list()
        raw_data = self.__db.get_data(
            f'SELECT area, region, deleted FROM area WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item is None:
                items.append('')
            else:
                items.append(raw_data[0][item])
        return items

    def users(self, row_id):
        items = list()
        raw_data = self.__db.get_data(
            f'SELECT role, full_name, date_create, email, phone_number, region, area, agent, blocked, password FROM users WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item == 1:
                fio = unparse_json(raw_data[0][item])
                items.extend(fio)
            elif item == 2:
                if raw_data[0][item] is None:
                    items.append('')
                else:
                    items.append(raw_data[0][item].strftime('%d-%m-%Y'))
            else:
                if raw_data[0][item] is None:
                    items.append('')
                else:
                    items.append(raw_data[0][item])
        return items

    def med_profile(self, row_id):
        items = list()
        temp = list()
        raw_data = self.__db.get_data(
            f'SELECT med_profile, deleted FROM med_profile WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item is None:
                items.append('')
            else:
                items.append(raw_data[0][item])
        raw_data = self.__db.get_data(
            f'SELECT id_ksg FROM relative_ksg_med_profile WHERE id_med_profile = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM ksg WHERE id = {i[0]}',
                ())
            temp.append(txt_data[0][0])
        items.insert(1, ', '.join(temp))
        return items

    def service(self, row_id):
        items = list()
        temp = list()
        temp1 = list()
        raw_data = self.__db.get_data(
            f'SELECT code, title, clinical_minimum, deleted FROM service WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item == 2:
                json_data = unparse_json(raw_data[0][2])
                for i in json_data:
                    for g in i:
                        items.append(g)
            else:
                items.append(raw_data[0][item])
        raw_data = self.__db.get_data(
            f'SELECT id_mkb FROM relative_mkb_service WHERE id_service = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM mkb WHERE id = {i[0]}',
                ())
            temp.append(txt_data[0][0])
        raw_data = self.__db.get_data(
            f'SELECT id_ksg FROM relative_ksg_service WHERE id_service = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM ksg WHERE id = {i[0]}',
                ())
            temp1.append(txt_data[0][0])
        items.insert(2, ', '.join(temp))
        items.insert(3, ', '.join(temp1))
        return items

    def ksg(self, row_id):
        items = list()
        temp = list()
        temp1 = list()
        temp2 = list()
        raw_data = self.__db.get_data(
            f'SELECT code, title, price, ratio, ratio_switch, deleted FROM ksg WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item == 3:
                json_data = unparse_json(raw_data[0][3])
                for i in json_data:
                    items.append(str(i))
            elif item == 4:
                if raw_data[0][4]:
                    items.append(True)
                else:
                    items.append(False)
            else:
                items.append(raw_data[0][item])
        raw_data = self.__db.get_data(
            f'SELECT id_mkb FROM relative_ksg_mkb WHERE id_ksg = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM mkb WHERE id = {i[0]}',
                ())
            temp.append(txt_data[0][0])
        raw_data = self.__db.get_data(
            f'SELECT id_mkb FROM relative_ksg_mkb WHERE id_ksg = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM service WHERE id = {i[0]}',
                ())
            temp1.append(txt_data[0][0])
        raw_data = self.__db.get_data(
            f'SELECT id_med_profile FROM relative_ksg_med_profile WHERE id_ksg = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT med_profile FROM med_profile WHERE id = {i[0]}',
                ())
            temp2.append(txt_data[0][0])
        items.insert(8, ', '.join(temp))
        items.insert(9, ', '.join(temp1))
        items.insert(10, ', '.join(temp2))
        return items

    def mkb(self, row_id):
        items = list()
        temp = list()
        temp1 = list()
        raw_data = self.__db.get_data(
            f'SELECT code, title, clinical_minimum, deleted FROM mkb WHERE id = {row_id}',
            ())
        for item in range(len(raw_data[0])):
            if item == 2:
                json_data = unparse_json(raw_data[0][2])
                for i in json_data:
                    for g in i:
                        items.append(g)
            else:
                items.append(raw_data[0][item])
        raw_data = self.__db.get_data(
            f'SELECT id_ksg FROM relative_ksg_mkb WHERE id_mkb = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM ksg WHERE id = {i[0]}',
                ())
            temp.append(txt_data[0][0])
        raw_data = self.__db.get_data(
            f'SELECT id_service FROM relative_mkb_service WHERE id_mkb = {row_id}',
            ())
        for i in raw_data:
            txt_data = self.__db.get_data(
                f'SELECT code FROM service WHERE id = {i[0]}',
                ())
            temp1.append(txt_data[0][0])
        items.insert(2, ', '.join(temp))
        items.insert(3, ', '.join(temp1))
        return items

    def hospital(self, row_id):
        items = list()
        raw_data = self.__db.get_data(
            f'SELECT name, med_profiles, moderator, ratio, base_rate, site, phone_number, email, other_contact, region, area, city, addres, requisites FROM hospital WHERE id = {row_id}', ())
        for item in range(len(raw_data[0])):
            if item == 8:
                json_data = unparse_json(raw_data[0][8])
                for i in json_data:
                    for g in i:
                        items.append(g)
            elif item == 1:
                json_data = unparse_json(raw_data[0][1])
                txt = ''
                for i in json_data:
                    txt += self.__db.get_data(f'SELECT med_profile FROM med_profile WHERE id = {i} AND deleted = 0', ())[0][0] + ', '
                items.append(txt)
            elif item == 13:
                json_data = unparse_json(raw_data[0][13])
                for i in json_data:
                    items.append(i)
            else:
                items.append(raw_data[0][item])
        return items

