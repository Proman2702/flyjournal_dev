"""
Парсер для:

проверка существования строки с указанной датой, профиля и номера
вывода csv формата одной строки



"""
# mode (delay/get/delete/save) - delay - отложить, get - заполнить, delete - удалить

# delay - перезаписывает не до конца заполненные данные в буфер сохранения в формат csv и ставит "" на месте отсутствующих данных

# get - сначала проверяет строку на наличие, потом ищет ее в буфере сохранения
# если строка имеется - выводит csv этой строки
# если строка в буфере - всплывает уведомление и выводится полный csv этой строки (со всеми данными)
# если строка не найдена - выводит '0'

# delete - удаляет указанную строку, если такая имеется, и возваращет новый csv, иначе выводит '0'

# save - сохраняет указанную строку (ПРОВЕРЯЕТ НА ОРИГИНАЛЬНОСТЬ) и возвращает новый csv, иначе выводит '1'

# num (1-5) - номер полета
# date (ДАТА ЧЕРЕЗ ПРОБЕЛ (ДД ММ ГГГГ)) - дата дня
# profile (строка) - профиль
# data - словарь
# big_data - csv файл данных



import pandas as pd
import datetime

class Parsing:
    def __init__(self, mode, num, date, profile, data, big_data):

        self.mode = mode
        self.num = num
        self.date = date
        self.profile = profile
        self.data = data
        self.big_data = big_data



    def main(self):
        if self.mode == 'delay':
            df = pd.DataFrame(
            columns=["profile", "date", "number", "plane_number", "flight", "place_departure", "place_arrival",
                     "place_arrival2",
                     "time_on", "time_off", "time_departure", "time_arrival", "time_PVP", "time_PPP", "ETD", "ETA",
                     "time_all", "time_air", "time_day", "time_night", "time_PVP_PPP_all", "ETD_ETA_all"]).to_csv(
            'buffer.csv', index=False)

            save = pd.read_csv('buffer.csv')
            save = save._append(self.data, ignore_index=True)
            save.to_csv('buffer.csv', sep=',', index=False)
            print('сохранено')
            return 1, save

        if self.mode == 'get':
            self.big_data['number'] = self.big_data['number'].astype(str)

            data = self.big_data[(self.big_data['profile'] == self.profile) &
                                 (self.big_data['number'] == self.num) &
                                 (self.big_data['date'] == self.date)]


            if len(data) == 0:
                data = pd.read_csv('buffer.csv')

                try:
                    data['number'] = data['number'].astype(str)
                    data = data[(data['profile'] == self.profile) &
                                (data['number'] == self.num) &
                                (data['date'] == self.date)]
                except:
                    return 0, ''

                if len(data) == 0:
                    return 0, ''
                else:
                    print('получено из буфера')
                    return 2, data

            else:
                print('Получено')
                return 1, data

        if self.mode == 'delete':
            try:
                self.big_data = (self.big_data.drop(self.big_data.index[(self.big_data['profile'] == self.profile) &
                                                               (self.big_data['number'] == self.num) &
                                                               (self.big_data['date'] == self.date)][0])
                                                               .reset_index(drop=True))
                self.big_data.to_csv("data.csv", sep=',', index=False)
                print('deleted')
                return 1, self.big_data
            except:
                print('not found')
                return 0, ''

        if self.mode == 'save':
            try:
                self.big_data.loc[self.big_data[(self.big_data['profile'] == self.profile) &
                                                (self.big_data['number'] == self.num) &
                                                (self.big_data['date'] == self.date)].index[0]] = self.data
                print('replaced')
            except:
                self.big_data = self.big_data._append(self.data, ignore_index=True)
                print('saved')

