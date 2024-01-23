import requests
import datetime as dt
import os
import sys
import time
import pandas as pd
import menu.profile
import calc.fly_time as fly_time


class Main:
    def __init__(self, command, commands):

        self.command = command

        self.available_commands = commands

    def execute(self):
        if self.command in self.available_commands:
            if self.command == '/stop':
                return self.stop()
            if self.command == '/help':
                return self.help()
        else:
            return "Неизвестная команда. Напишите /help для просмотра списка команд"

    def help(self):
        print(f"Доступные команды: {self.available_commands}")

    def stop(self):
        print('Остановка программы...')
        return exit()


if __name__ == '__main__':
    # Стартовое меню
    on_start_menu = False
    # Меню редактирования полетов по дате
    on_data_menu = False
    # Меню редактирования полета
    on_flight_menu = False
    # Главное меню
    on_main_menu = True

    # Создание файла с профилями, если приложение открыто в первый раз
    if not os.path.exists("profiles.csv"):
        df = pd.DataFrame(
            columns=["profile_name", "fio", "company", "flytime_all", "flytime_day", "flytime_night", "add_all", "add_day", "add_night"]).to_csv(
            'profiles.csv', index=False)

    if not os.path.exists("data.csv"):
        df2 = pd.DataFrame(
            columns=["profile", "date", "number", "plane_number", "flight", "place_departure", "place_arrival",
                     "place_arrival2",
                     "time_on", "time_off", "time_departure", "time_arrival", "time_PVP", "time_PPP", "ETD", "ETA",
                     "time_all", "time_air", "time_day", "time_night", "time_PVP_PPP_all", "ETD_ETA_all"]).to_csv(
            'data.csv', index=False)

    default_commands = ['/stop', '/help']
    main_menu_commands = ['/get_profile', '/get_profile_info', '/greeting', '/change', '/add']
    data_menu_commands = ['/flight 1', '/flight 2', '/flight 3', '/flight 4', '/flight 5', '/date', '/return', '/flights', '/delflight 1', '/delflight 2', '/delflight 3', '/delflight 4', '/delflight 5']
    start_menu_commands = ['/set_profile']

    profile = menu.profile.Profile(command='/set_profile', commands=default_commands + start_menu_commands).execute()
    date = ' '.join(map(str, [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]))

    # -----------------------------------------
    import menu.main_menu
    import menu.data

    menu.main_menu.Main_Menu('/greeting', default_commands + main_menu_commands, profile, date).execute()

    while True:

        command = input()

        if on_start_menu:  #Меню профилей
            if command == '/set_profile':
                on_main_menu = True
                on_start_menu = False
                profile = menu.profile.Profile(command, default_commands + start_menu_commands).execute()

                menu.main_menu.Main_Menu('/greeting', default_commands + main_menu_commands, profile, date).execute()
            else:
                menu.profile.Profile(command, default_commands + start_menu_commands).execute()

        if on_data_menu:  #Меню полетов

            if command == '/date':
                date = input("Введите дату в формате ГГГГ ММ ДД (через пробел): ")

            menu.data.Data_Menu(command, default_commands + data_menu_commands, profile, date).execute()

            if command == '/flight 1' or command == '/flight 2' or command == '/flight 3' or command == '/flight 4' or command == '/flight 5' or command == '/return':
                on_main_menu = True
                on_data_menu = False
                menu.main_menu.Main_Menu('/greeting', default_commands + main_menu_commands, profile, date).execute()
                date = ' '.join(map(str, [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]))

        if on_main_menu and command != '/set_profile' and command != '/flight 1' and command != '/flight 2' and command != '/flight 3' and command != '/flight 4' and command != '/flight 5' and command != '/return':

            if command == '/change':  #Главное меню
                on_main_menu = False
                on_start_menu = True

            if command == '/add':
                on_main_menu = False
                on_data_menu = True

            menu.main_menu.Main_Menu(command, default_commands + main_menu_commands, profile, date).execute()

# a = fly_time.TimeResult('IST', 'KZN', '13 05', '17 35')
# print(a.night_time, a.day_time)