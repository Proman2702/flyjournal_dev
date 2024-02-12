import pandas as pd
import datetime as dt
import calc.time_parser
import calc.data_parser
from itertools import permutations, product


data_filled = {"profile": 1,  # профиль
                       "date": 1,  # дата
                       "number": 1,  # номер (в день до 5)
                       "plane_number": 0,  # номер самолета
                       "flight": 1,  # номер рейса
                       "place_departure": 0,  # место отправления
                       "place_arrival": 0,  # место прибытия
                       "place_arrival2": '',  # запасной (неактивный/активный)
                       "time_on": '',  # время включения двигателей (ДЛЯ РАСЧЕТА)
                       "time_off": '',  # время выключения двигателей (ДЛЯ РАСЧЕТА)
                       "time_departure": 0,  # время отрыва колес
                       "time_arrival": 0,  # время приземления
                       "time_PVP": '',  # время (неактивный/активный)
                       "time_PPP": '',  # время (неактивный/активный)
                       "ETD": '',  # во сколько должны были взлететь
                       "ETA": '',  # во сколько должны были сесть
                       "time_all": 0,  # общее время от вкл до выкл (ДЛЯ РАСЧЕТА)
                       "time_air": '',  # общее время в воздухе
                       "time_day": 0,  # от общего времени
                       "time_night": 0,  # от общего времени
                       "time_PVP_PPP_all": '',  # ничего нет
                       "ETD_ETA_all": ''}  # суммирование etd + eta

csv = pd.DataFrame({"date": ['02 12 2023', '01 01 2024', '02 01 2024', '07 01 2024'],
                    "time_night": ['2:00:00', '1:30:00', '0:20:00', '1:00:00'],
                    'time_day': ['2:00:00', '1:30:00', '0:20:00', '1:00:00'],
                    "time_all": ['4:00:00', '3:00:00', '0:40:00', '2:00:00'],
                    "profile": ['uz', 'uz', 'uz', 'uz'],
                    "number": ['1', '0', '2', '2']})


parser = calc.data_parser.Parsing(mode='get', big_data=csv, date='02 01 2024', data=data_filled, num='2', profile='uz').main()


print(parser)









