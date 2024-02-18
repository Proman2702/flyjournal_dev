import pandas as pd
import datetime as dt
import calc.time_parser
import calc.data_parser
import calc.fly_time
from itertools import permutations, product


data_filled = {"profile": 'uz',  # профиль
                       "date": '1 02 2024',  # дата
                       "number": 1,  # номер (в день до 5)
                       "plane_number": 'ffdss',  # номер самолета
                       "flight": 'dsf',  # номер рейса
                       "place_departure": 'VKO',  # место отправления
                       "place_arrival": 'TJM',  # место прибытия
                       "place_arrival2": '',  # запасной (неактивный/активный)
                       "time_on": '12:00:00',  # время включения двигателей (ДЛЯ РАСЧЕТА)
                       "time_off": '17:00:00',  # время выключения двигателей (ДЛЯ РАСЧЕТА)
                       "time_departure": '12:20:00',  # время отрыва колес
                       "time_arrival": '16:40:00',  # время приземления
                       "time_PVP": '',  # время (неактивный/активный)
                       "time_PPP": '',  # время (неактивный/активный)
                       "ETD": '12:00:00',  # во сколько должны были взлететь
                       "ETA": '17:00:00', # во сколько должны были сесть
                       "time_all": 0,  # общее время от вкл до выкл (ДЛЯ РАСЧЕТА)
                       "time_air": '',  # общее время в воздухе
                       "time_day": 0,  # от общего времени
                       "time_night": 0,  # от общего времени
                       "time_PVP_PPP_all": '',  # ничего нет
                       "ETD_ETA_all": ''}  # суммирование etd + eta



#parser = calc.data_parser.Parsing(mode='get', big_data=csv, date='02 01 2024', data=data_filled, num='2', profile='uz').main()

def time_vision(t):
    h = t.split(" ")[0]
    m = t.split(" ")[1]
    s = '00'

    if len(h) == 1:
        h = "0" + h
    if len(m) == 1:
        m = "0" + m

    return f"{h}:{m}:{s}"


def date_formation(d):
    d = d.split(' ')
    d = d[::-1]
    tmp = " ".join(d)
    return tmp


print(date_formation('12 05 2020'))

#print(parser)










