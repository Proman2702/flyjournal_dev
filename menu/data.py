import main
import pandas as pd
import datetime as dt
import calc.fly_time as fly_time


class Data_Menu(main.Main):

    def __init__(self, command, commands, profile, date):

        self.data = pd.read_csv("data.csv", index_col=0)
        self.profiles = pd.read_csv("profiles.csv", index_col=0)

        super().__init__(command, commands)
        self.profile = profile
        self.date = date

    def execute(self):

        if self.command in self.available_commands:
            if (self.command == '/flight 1' or
                    self.command == '/flight 2' or
                    self.command == '/flight 3' or
                    self.command == '/flight 4' or
                    self.command == '/flight 5'):
                return self.add_flight()
            if (self.command == '/delflight 1' or
                    self.command == '/delflight 2' or
                    self.command == '/delflight 3' or
                    self.command == '/delflight 4' or
                    self.command == '/delflight 5'):
                return self.delete_flight()

            if self.command == '/date':
                return self.set_date()

            if self.command == '/return':
                return self.return_to()

            if self.command == '/flights':
                return self.flights_info()

            else:
                return super().execute()

        else:
            print("Неизвестная команда. Напишите /help для просмотра списка команд")

    def time_absolute(self, time):
        time = list(map(int, time.split()))
        return round(time[0] + time[1] / 60, 2)

    def fill_data(self, num):

        print('=============== Cтраница редактирования полетов ===============')
        print('----------------------------')
        print('Введите данные для заполнения информации о полете:')
        print('----------------------------')
        code = "IATA"

        plane = input("Введите номер самолета: ")
        way = input("Введите номер рейса: ")

        departure_place = input(f'Введите место отправления ({code}): ')
        arrival_place = input(f'Введите место прибытия ({code}): ')

        # h = input(f'Введите другое место прибытия ({code}) (если его нет, нажмите Enter): ')
        # i = input("Введите время запуска двигателей (формат через пробел ЧАСЫ МИНУТЫ): ")
        # j = input("Введите время выключения двигателей (формат через пробел ЧАСЫ МИНУТЫ): ")

        departure_time = input('Время отправления (формат через пробел ЧАСЫ МИНУТЫ): ')
        arrival_time = input('Время прибытия (формат через пробел ЧАСЫ МИНУТЫ): ')

        # m = input("Enter ")
        # n = input("Enter ")
        # o = input("Enter ")
        # p = input("Enter ")

        print('Идет запись...')
        print('[............]')
        all_time = fly_time.TimeResult(departure=departure_place, arrival=arrival_place, d=departure_time,
                                       a=arrival_time, date=self.date).all_time
        print('[|||.........]')
        day_time = fly_time.TimeResult(departure=departure_place, arrival=arrival_place, d=departure_time,
                                       a=arrival_time, date=self.date).day_time
        print('[||||||......]')
        night_time = fly_time.TimeResult(departure=departure_place, arrival=arrival_place, d=departure_time,
                                         a=arrival_time, date=self.date).night_time
        print('[|||||||||...]')

        all_time = self.time_absolute(" ".join(map(str, [all_time.seconds // 3600, all_time.seconds // 60 % 60])))
        day_time = self.time_absolute(" ".join(map(str, [day_time.seconds // 3600, day_time.seconds // 60 % 60])))
        night_time = self.time_absolute(" ".join(map(str, [night_time.seconds // 3600, night_time.seconds // 60 % 60])))

        data_filled = {"profile": self.profile,  # a
                       "date": self.date,  # b
                       "number": num,  # c
                       "plane_number": plane,  # d
                       "flight": way,  # e
                       "place_departure": departure_place,  # f
                       "place_arrival": arrival_place,  # g
                       "place_arrival2": '',  # запасной (неактивный/активный)
                       "time_on": '',  # время включения двигателей (ДЛЯ РАСЧЕТА)
                       "time_off": '',  # время выключения двигателей (ДЛЯ РАСЧЕТА)
                       "time_departure": departure_time,  # время отрыва колес
                       "time_arrival": arrival_time,  # время приземления
                       "time_PVP": '',  # время (неактивный/активный)
                       "time_PPP": '',  # время (неактивный/активный)
                       "ETD": '',  # во сколько должны были взлететь
                       "ETA": '',  # во сколько должны были сесть
                       "time_all": all_time,  # общее время от вкл до выкл (ДЛЯ РАСЧЕТА)
                       "time_air": '',  # общее время в воздухе
                       "time_day": day_time,  # от общего времени
                       "time_night": night_time,  # от общего времени
                       "time_PVP_PPP_all": '',  # ничего нет
                       "ETD_ETA_all": ''}  # суммирование etd + eta

        try:
            self.data.loc[self.data[(self.data['profile'] == self.profile) & (self.data['number'] == num) & (
                    self.data['date'] == self.date)].index[0]] = data_filled
        except:
            self.data = self.data._append(data_filled, ignore_index=True)

        self.profile_calc()

        print('[||||||||||||]')
        self.profiles.to_csv("profiles.csv", sep=',')
        self.data.to_csv("data.csv", sep=',')

    def profile_calc(self):
        self.profiles.iloc[
            self.profiles[self.profiles['profile_name'] == self.profile].index[0], self.profiles.columns.get_loc(
                "flytime_all")] = self.data.loc[self.data[(self.data['profile'] == self.profile)].index][
            'time_all'].sum()
        self.profiles.iloc[
            self.profiles[self.profiles['profile_name'] == self.profile].index[0], self.profiles.columns.get_loc(
                "flytime_day")] = self.data.loc[self.data[(self.data['profile'] == self.profile)].index][
            'time_day'].sum()
        self.profiles.iloc[
            self.profiles[self.profiles['profile_name'] == self.profile].index[0], self.profiles.columns.get_loc(
                "flytime_night")] = self.data.loc[self.data[(self.data['profile'] == self.profile)].index][
            'time_night'].sum()

    def add_flight(self):
        self.fill_data(int(self.command.split()[1]))
        print("Данные сохранены!")

    def delete_flight(self):
        n = int(self.command.split()[1])
        self.data = self.data.drop(self.data.index[(self.data['profile'] == self.profile) &
                                                   (self.data['number'] == n) &
                                                   (self.data['date'] == self.date)][0]).reset_index(drop=True)
        self.data.to_csv("data.csv", sep=',')

        self.profile_calc()

        self.profiles.to_csv("profiles.csv", sep=',')
        self.data.to_csv("data.csv", sep=',')

        print(f"Полет номер {n} удален!")

    def set_date(self):
        print(f'Дата установлена на {self.date}')

    def return_to(self):
        print('Выход в главное меню...')

    def flights_info(self):
        print('--------------------------------------------')

        try:
            n1 = self.data.index[(self.data['profile'] == self.profile) &
                                 (self.data['number'] == 1) &
                                 (self.data['date'] == self.date)][0]
            print(
                f"{self.data.at[n1, 'time_departure']} | {self.data.at[n1, 'place_departure']} ---> {self.data.at[n1, 'place_arrival']} | {self.data.at[n1, 'time_arrival']}")
        except:
            print('Полет 1: <нет>')

        try:
            n2 = self.data.index[(self.data['profile'] == self.profile) &
                                 (self.data['number'] == 2) &
                                 (self.data['date'] == self.date)][0]
            print(
                f"{self.data.at[n2, 'time_departure']} | {self.data.at[n2, 'place_departure']} ---> {self.data.at[n2, 'place_arrival']} | {self.data.at[n2, 'time_arrival']}")
        except:
            print(f'Полет 2: <нет>')

        try:
            n3 = self.data.index[(self.data['profile'] == self.profile) &
                                 (self.data['number'] == 3) &
                                 (self.data['date'] == self.date)][0]
            print(
                f"{self.data.at[n3, 'time_departure']} | {self.data.at[n3, 'place_departure']} ---> {self.data.at[n3, 'place_arrival']} | {self.data.at[n3, 'time_arrival']}")
        except:
            print(f'Полет 3: <нет>')

        try:
            n4 = self.data.index[(self.data['profile'] == self.profile) &
                                 (self.data['number'] == 4) &
                                 (self.data['date'] == self.date)][0]
            print(
                f"{self.data.at[n4, 'time_departure']} | {self.data.at[n4, 'place_departure']} ---> {self.data.at[n4, 'place_arrival']} | {self.data.at[n4, 'time_arrival']}")
        except:
            print(f'Полет 4: <нет>')

        try:
            n5 = self.data.index[(self.data['profile'] == self.profile) &
                                 (self.data['number'] == 5) &
                                 (self.data['date'] == self.date)][0]
            print(
                f"{self.data.at[n5, 'time_departure']} | {self.data.at[n5, 'place_departure']} ---> {self.data.at[n5, 'place_arrival']} | {self.data.at[n5, 'time_arrival']}")
        except:
            print(f'Полет 5: <нет>')

        print('--------------------------------------------')
