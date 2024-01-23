import main
import pandas as pd
import datetime
import menu.profile


class Main_Menu(main.Main):

    def __init__(self, command, commands, profile, date):

        super().__init__(command, commands)
        self.profile = profile
        self.profiles = pd.read_csv("profiles.csv", index_col=0)
        self.data = pd.read_csv('data.csv', index_col=0)
        self.date = date

    def execute(self):
        if self.command in self.available_commands:
            if self.command == '/get_profile':
                return self.get()
            elif self.command == '/get_profile_info':
                return self.info()
            elif self.command == '/greeting':
                return self.greetings()
            elif self.command == '/add':
                return self.add()
            elif self.command == '/change':
                return self.change_profile()
            else:
                return super().execute()
        else:
            print("Неизвестная команда. Напишите /help для просмотра списка команд")

    def get(self):
        print(self.profile)

    def add(self):
        print("========= Добро пожаловать на страницу редактирования полетов =========")
        print(f"Установленная дата: {self.date}")
        print("/flight (1,2,3,4,5) для добавления/редактирования полета")
        print("/delflight (1,2,3,4,5) для удаления полета")
        print("/flights - информация о полетах")
        print("/date - изменить дату")
        print("/return - вернуться в главное меню")

    def change_profile(self):
        print("Введите /set_profile, чтобы сменить профиль")

    def info(self):

        print(self.profiles.loc[self.profiles['profile_name'] == self.profile])

    # print
    def greetings(self):

        profile_ind = self.profiles.index[self.profiles['profile_name'] == self.profile][0]

        print('======= Добро пожаловать на главную страницу приложения! =======')
        print(f'Дата: {datetime.datetime.now()}')
        print('--------------------------------------------')
        print(f'ФИО: {self.profiles.at[profile_ind, "fio"]}')
        print(f'ЧАСЫ НАЛЕТА: {self.profiles.at[profile_ind, "flytime_all"] + self.profiles.at[profile_ind, "add_all"]}')
        print('--------------------------------------------')
        print('/get_profile_info - посмотреть детали профиля')
        print('/add - зайти в меню редактирования полетов')
        print('/change - изменить профиль')

