import requests
import airportsdata
import datetime as dt


airports = airportsdata.load("IATA")

# Подсказка #

# Обращаться только к классу TimeResult!!!!!!
'''
d - время вылета
a - время прилета
mid_sns - средний закат
mid_snr - средний восход
res_night - время ночного полета
res_day - время дневного полета
all_time - общее время полета
snr1, sns1 - восход/закат пункта вылета
snr2, sns2 - восход/закат пункта прилета

.seconds // 3600 - часы, .seconds // 60 % 60 - минуты
'''

'''
Формат ввода: 

TimeResult(1, 2, 3, 4, 5)
1 - 3х-значный код аэропорта вылета (IATA)
2 - 3х-значный код аэропорта посадки (IATA)
3 - время (ЧАСЫ МИНУТЫ через пробел) вылета
4 - время (ЧАСЫ МИНУТЫ через пробел) посадки
5 - дата (ГОД МЕСЯЦ ДЕНЬ через пробел)
'''

'''
Функции класса TimeCalculation (подробности в коде):

1. Конвертирование времени
2. Общее время
3. Время восхода/заката
4. Среднее время
'''


class TimeCalculation:
    # расчет общего времени полета (dt взлет, dt посадка)
    @staticmethod
    def time_summary(t1, t2):
        if t2 >= t1:
            res = t2 - t1
        else:
            res = dt.timedelta(hours=24, minutes=00) - (t1 - t2)

        return res

    # расчет времени восхода/заката для аэропорта (IATA код)
    @staticmethod
    def get_snr_and_sns(dest, date):

        def time_formation(t):
            tmp = t.split(":")
            if t[-1:-3:-1] == 'MP':

                if tmp[0] == '12':
                    tmp[0] = '12'
                else:
                    tmp[0] = str(int(tmp[0]) + 12)
            tmp[2] = tmp[2][:-3]
            t = tmp
            return t

        def date_formation(d):
            tmp = d.replace(" ", '-')
            return tmp

        lat, lon = airports[dest]['lat'], airports[dest]['lon']
        date = date_formation(date)

        r = requests.get(f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}")
        # print(r.json())
        snr = time_formation(r.json()['results']['sunrise'])
        sns = time_formation(r.json()['results']['sunset'])

        return [snr, sns]

    # расчет среднего арифм. времени (dt 1 время, dt 2 время)
    @staticmethod
    def time_mid(t1, t2):

        res = (t1 + t2) // 2

        if (max(t1, t2) - min(t1, t2)) > dt.timedelta(hours=12):
            res += dt.timedelta(hours=12)

        if res >= dt.timedelta(days=1):
            res -= dt.timedelta(days=1)

        return res

    # перевод из строки в dt время (часы пробел минуты, False)
    @staticmethod
    def time_rewrite(t, List):
        if List:
            t[0], t[1] = list(map(int, t[0])), list(map(int, t[1]))

            return dt.timedelta(hours=t[0][0], minutes=t[0][1], seconds=t[0][2]), dt.timedelta(
                hours=t[1][0], minutes=t[1][1], seconds=t[1][2])
        if not List:
            t = t.split()
            return dt.timedelta(hours=int(t[0]), minutes=int(t[1]))


class TimeResult(TimeCalculation):
    def __init__(self, departure, arrival, d, a, date, code):

        global airports
        airports = airportsdata.load(code)

        # список восход/закат пункта вылета
        self.snr1, self.sns1 = self.time_rewrite(self.get_snr_and_sns(departure, date), List=True)
        # список восход/закат пункта прилета
        self.snr2, self.sns2 = self.time_rewrite(self.get_snr_and_sns(arrival, date), List=True)

        # время вылета
        self.d = self.time_rewrite(d, List=False)
        # время прилета
        self.a = self.time_rewrite(a, List=False)
        # средний восход
        self.mid_snr = self.time_mid(self.snr1, self.snr2)
        # средний закат
        self.mid_sns = self.time_mid(self.sns1, self.sns2)
        # общее время полета
        self.all_time = self.time_summary(self.d, self.a)

        self.night_time, self.day_time = self.time_logic()

    def time_logic(self):
        res_night = dt.timedelta()

        # вылет между закатом и 0 часами
        if self.mid_sns < self.d <= dt.timedelta(hours=24, minutes=00):
            # прилет между 0 часами и восходом
            if dt.timedelta(hours=0, minutes=0) <= self.a < self.mid_snr:
                res_night = dt.timedelta(hours=24, minutes=00) - self.d + self.a
            # прилет между закатом и 0 часами
            elif self.d < self.a <= dt.timedelta(hours=24, minutes=00) and self.mid_sns < self.a <= dt.timedelta(hours=23, minutes=59):
                res_night = self.a - self.d
            # прилет между восходом и закатом
            elif self.mid_snr <= self.a <= self.mid_sns:
                res_night = dt.timedelta(hours=24, minutes=00) - self.d + self.mid_snr

        # вылет между 0 часами и восходом
        elif dt.timedelta(hours=0, minutes=0) <= self.d < self.mid_snr:
            # прилет между 0 часами и восходом
            if dt.timedelta(hours=0, minutes=0) <= self.a < self.mid_snr:
                res_night = self.a - self.d
            # прилет между закатом и 0 часами
            elif self.d < self.a <= dt.timedelta(hours=24, minutes=00) and self.mid_sns < self.a <= dt.timedelta(hours=23, minutes=59):
                res_night = self.mid_snr - self.d + self.a - self.mid_sns
            # прилет между восходом и закатом
            elif self.mid_snr <= self.a <= self.mid_sns:
                res_night = self.mid_snr - self.d

        # вылет между восходом и закатом:
        elif self.mid_snr <= self.d <= self.mid_sns:
            # прилет между 0 часами и восходом
            if dt.timedelta(hours=0, minutes=0) <= self.a < self.mid_snr:
                res_night = dt.timedelta(hours=24, minutes=00) - self.mid_sns + self.a
            # прилет между закатом и 0 часами
            elif self.d < self.a <= dt.timedelta(hours=24, minutes=00) and self.mid_sns < self.a <= dt.timedelta(hours=23, minutes=59):
                res_night = self.a - self.mid_sns
            # прилет между восходом и закатом
            elif self.mid_snr <= self.a <= self.mid_sns:
                res_night = dt.timedelta(hours=0, minutes=0)

        res_day = self.time_summary(self.d, self.a) - res_night

        return res_night, res_day
