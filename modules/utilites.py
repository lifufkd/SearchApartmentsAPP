#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import datetime
import json
import os
import parawrap
import xlwt
from time import gmtime, strftime
############static variables#####################

#################################################


def get_rtc():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def get_data_main_page(db):
    cat_quantity = {'ksg': 0, 'mkb': 0, 'service': 0, 'region': 0, 'area': 0, 'med_profile': 0, 'users': 0}
    temp = list()
    for cat in cat_quantity.keys():
        if cat == 'users':
            for role in range(4):
                temp.append(db.get_quantity(cat, ['role', role]))
            cat_quantity[cat] = temp  # 0 - admin, 1 - moderator, 2 - curator, 3 - user
        else:
            cat_quantity[cat] = db.get_quantity(cat)
    return cat_quantity


def unparse_json(data):
    return json.loads(data)


def parse_json(data):
    return json.dumps(data, ensure_ascii=False)


def update_profile(new_data, old_data, db):
    out = list()
    f_old = old_data[0:2] + [old_data[5]]
    compare = {0: 'login', 1: 'full_name', 2: 'password'}
    for diff in range(len(new_data)):
        if diff == 1:
            out.append([])
            for i in range(len(new_data[diff])):
                if new_data[diff][i] != '':
                    out[diff].append(new_data[diff][i])
                else:
                    out[diff].append(f_old[diff][i])
            db.add_db_entry(f'UPDATE users SET {compare[diff]} = %s WHERE id = {old_data[4]}', (parse_json(out[diff]), ))
        else:
            if new_data[diff] != '':
                out.append(new_data[diff])
                db.add_db_entry(f'UPDATE users SET {compare[diff]} = %s WHERE id = %s', (new_data[diff], old_data[5]))
            else:
                out.append(f_old[diff])
    for i in range(3):
        out.insert(i + 2, old_data[i + 2])
    return out


def word_wrap(text, max_len):
    s = ''
    data = parawrap.wrap(text, max_len)
    for i in data:
        s += i + '\n'
    return s


def save_export_xlsx(path, data, typ):
    if not os.path.exists(path):
        os.mkdir(path)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet")
    for i in range(len(data)):
        for j in range(len(data[i])):
            sheet.write(i, j, data[i][j])
    workbook.save(path + f'export_{typ}({strftime("%Y_%m_%d_%H_%M_%S", gmtime())}).xlsx')


def switch_btns_user(data, value, db):
    fields = {'1': 'agent', '2': 'blocked'}
    db.add_db_entry(f'UPDATE users SET {fields[data[1]]} = {value} WHERE id = "{data[0]}"', ())


def switch_btns_ksg(data, value, db):
    db.add_db_entry(f'UPDATE ksg SET ratio_switch = {value} WHERE id = "{data}"', ())


def delete_row(db, data):
    for i, g in data.items():
        db.add_db_entry(f'UPDATE {i} SET deleted = 1 WHERE {g[0]} = "{g[1]}"', ())


def insert_data_application(db, table, data):
    db.add_db_entry(f'INSERT INTO {table} (number, application_type, payment_type, application_status, close_author, patient, mkb, service, сhronic_diseases, comment_designer, comment_tutor, file, price, application_author, hospitalized, hospital, ratio, status, date_create, date_notice, date_hospitalized, date_close, deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)


def update_data_application(db, table, data, row_id):
    db.add_db_entry(f'UPDATE {table} SET number = %s, application_type = %s, payment_type = %s, application_status = %s, close_author = %s, patient = %s, mkb = %s, service = %s, сhronic_diseases = %s, comment_designer = %s, comment_tutor = %s, file = %s, price = %s, application_author = %s, hospitalized = %s, hospital = %s, ratio = %s, status = %s, date_create = %s, date_notice = %s, date_hospitalized = %s, date_close = %s, deleted = %s WHERE id = {row_id}', data)


def insert_data_area(db, table, data):
    db.add_db_entry(f'INSERT INTO {table} (area, region, deleted) VALUES (%s, %s, %s)', data)


def update_data_area(db, table, data, row_id):
    db.add_db_entry(f'UPDATE {table} SET area = %s, region = %s, deleted = %s WHERE id = {row_id}', data)


def insert_data_users(db, table, data):
    db.add_db_entry(f'INSERT INTO {table} (role, full_name, date_create, email, phone_number, region, area, agent, blocked, password, deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)


def update_data_users(db, table, data, row_id):
    db.add_db_entry(f'UPDATE {table} SET role = %s, full_name = %s, date_create = %s, email = %s, phone_number = %s, region = %s, area = %s, agent = %s, blocked = %s, password = %s, deleted = %s WHERE id = {row_id}', data)


def insert_data_med_profile(db, data):
    temp = list()
    db.add_db_entry(f'INSERT INTO med_profile (med_profile, deleted) VALUES (%s, %s)', (data[0], 0))
    med_profile = db.get_data(f'SELECT MAX(id) FROM med_profile', ())[0][0]
    for i in data[1]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        db.add_db_entry(f'INSERT INTO relative_ksg_med_profile (id_ksg, id_med_profile, deleted) VALUES (%s, %s, %s)', (i, med_profile, 0))


def update_data_med_profile(db, data, row_id):
    temp = list()
    db.add_db_entry(f'UPDATE med_profile SET med_profile = %s, deleted = %s WHERE id = %s', (data[0], 0, row_id))
    for i in data[1]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_ksg, id_med_profile FROM relative_ksg_med_profile WHERE id_ksg = %s AND id_med_profile = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_med_profile (id_ksg, id_med_profile, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))


def insert_data_service(db, data):
    temp = list()
    temp1 = list()
    db.add_db_entry(f'INSERT INTO service (code, title, clinical_minimum, deleted) VALUES (%s, %s, %s, %s)', (data[0], data[1], data[4], data[5]))
    new_id = db.get_data(f'SELECT MAX(id) FROM service', ())[0][0]
    for i in data[2]:
        ids = db.get_data(f'SELECT id FROM mkb WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        db.add_db_entry(f'INSERT INTO relative_mkb_service (id_mkb, id_service, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))
    for i in data[3]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        db.add_db_entry(f'INSERT INTO relative_ksg_service (id_ksg, id_service, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))


def update_data_service(db, data, row_id):
    temp = list()
    temp1 = list()
    db.add_db_entry(f'UPDATE service SET code = %s, title = %s, clinical_minimum = %s, deleted = %s WHERE id = %s', (data[0], data[1], data[4], data[5], row_id))
    for i in data[2]:
        ids = db.get_data(f'SELECT id FROM mkb WHERE code = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_mkb, id_service FROM relative_mkb_service WHERE id_mkb = %s AND id_service = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_mkb_service (id_mkb, id_service, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))
    for i in data[3]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_ksg, id_service FROM relative_ksg_service WHERE id_ksg = %s AND id_service = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_service (id_ksg, id_service, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))

def insert_data_ksg(db, data):
    temp = list()
    temp1 = list()
    temp2 = list()
    db.add_db_entry(f'INSERT INTO ksg (code, title, price, ratio, ratio_switch, deleted) VALUES (%s, %s, %s, %s, %s, %s)', (data[0], data[1], data[2], data[3], data[4], data[8]))
    new_id = db.get_data(f'SELECT MAX(id) FROM ksg', ())[0][0]
    for i in data[5]:
        ids = db.get_data(f'SELECT id FROM mkb WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        db.add_db_entry(f'INSERT INTO relative_ksg_mkb (id_mkb, id_ksg, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))
    for i in data[6]:
        ids = db.get_data(f'SELECT id FROM service WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        db.add_db_entry(f'INSERT INTO relative_ksg_service (id_service, id_ksg, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))
    for i in data[7]:
        ids = db.get_data(f'SELECT id FROM med_profile WHERE med_profile = %s', (i, ))
        if len(ids) > 0:
            temp2.append(ids[0][0])
    for i in temp2:
        db.add_db_entry(f'INSERT INTO relative_ksg_med_profile (id_med_profile, id_ksg, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))


def update_data_ksg(db, data, row_id):
    temp = list()
    temp1 = list()
    temp2 = list()
    db.add_db_entry(f'UPDATE ksg SET code = %s, title = %s, price = %s, ratio = %s, ratio_switch = %s WHERE id = %s', (data[0], data[1], data[2], data[3], data[4], row_id))
    for i in data[5]:
        ids = db.get_data(f'SELECT id FROM mkb WHERE code = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_mkb, id_ksg FROM relative_ksg_mkb WHERE id_mkb = %s AND id_ksg = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_mkb (id_mkb, id_ksg, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))
    for i in data[6]:
        ids = db.get_data(f'SELECT id FROM service WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_service, id_ksg FROM relative_ksg_service WHERE id_service = %s AND id_ksg = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_service (id_service, id_ksg, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))
    for i in data[7]:
        ids = db.get_data(f'SELECT id FROM med_profile WHERE med_profile = %s', (i, ))
        if len(ids) > 0:
            temp2.append(ids[0][0])
    for i in temp2:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_med_profile, id_ksg FROM relative_ksg_med_profile WHERE id_med_profile = %s AND id_ksg = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_med_profile (id_med_profile, id_ksg, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))

def insert_data_mkb(db, data):
    temp = list()
    temp1 = list()
    db.add_db_entry(f'INSERT INTO mkb (code, title, clinical_minimum, deleted) VALUES (%s, %s, %s, %s)', (data[0], data[1], data[4], data[5]))
    new_id = db.get_data(f'SELECT MAX(id) FROM mkb', ())[0][0]
    for i in data[2]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        db.add_db_entry(f'INSERT INTO relative_ksg_mkb (id_ksg, id_mkb, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))
    for i in data[3]:
        ids = db.get_data(f'SELECT id FROM service WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        db.add_db_entry(f'INSERT INTO relative_mkb_service (id_service, id_mkb, deleted) VALUES (%s, %s, %s)', (i, new_id, 0))


def update_data_mkb(db, data, row_id):
    temp = list()
    temp1 = list()
    db.add_db_entry(f'UPDATE mkb SET code = %s, title = %s, clinical_minimum = %s, deleted = %s WHERE id = %s', (data[0], data[1], data[4], data[5], row_id))
    for i in data[2]:
        ids = db.get_data(f'SELECT id FROM ksg WHERE code = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    for i in temp:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_ksg, id_mkb FROM relative_ksg_mkb WHERE id_ksg = %s AND id_mkb = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_ksg_mkb (id_ksg, id_mkb, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))
    for i in data[3]:
        ids = db.get_data(f'SELECT id FROM service WHERE code = %s', (i, ))
        if len(ids) > 0:
            temp1.append(ids[0][0])
    for i in temp1:
        stat = db.get_data(f'SELECT EXISTS(SELECT id_service, id_mkb FROM relative_mkb_service WHERE id_service = %s AND id_mkb = %s)', (i, row_id))[0][0]
        if stat == 0:
            db.add_db_entry(f'INSERT INTO relative_mkb_service (id_service, id_mkb, deleted) VALUES (%s, %s, %s)',
                            (i, row_id, 0))


def insert_data_hospital(db, data):
    temp = list()
    for i in data[1]:
        ids = db.get_data(f'SELECT id FROM med_profile WHERE med_profile = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    data[1] = parse_json(temp)
    db.add_db_entry(f'INSERT INTO hospital (name, med_profiles, moderator, ratio, base_rate, site, '
                    f'phone_number, email, other_contact, region, area, city, addres, requisites, deleted) '
                    f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)


def update_data_hospital(db, data, row_id):
    temp = list()
    for i in data[1]:
        ids = db.get_data(f'SELECT id FROM med_profile WHERE med_profile = %s', (i,))
        if len(ids) > 0:
            temp.append(ids[0][0])
    data[1] = parse_json(temp)
    db.add_db_entry(f'UPDATE hospital SET name = %s, med_profiles = %s, moderator = %s, ratio = %s, base_rate = %s, '
                    f'site = %s, phone_number = %s, email = %s, other_contact = %s, region = %s, area = %s, city = %s ,'
                    f' addres = %s, requisites = %s, deleted = %s WHERE id = {row_id}', data)





