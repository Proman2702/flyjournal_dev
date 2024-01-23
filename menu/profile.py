import main
import pandas as pd

class Profile(main.Main):

    def execute(self):
        if self.command in self.available_commands:
            if self.command == '/set_profile':
                return self.set_profile()
            else:
                return super().execute()
        else:
            return "Неизвестная команда. Напишите /help для просмотра списка команд"

    def set_profile(self):
        profiles = pd.read_csv("profiles.csv", index_col=0)

        print('Выберете профиль: (если хотите создать новый профиль, нажмите enter)')
        print('---------------------')

        if len(profiles) > 0:
            for i in range(len(profiles)):
                print(f'Профиль №{i + 1}: {profiles.iloc[i, profiles.columns.get_loc("profile_name")]}')
        else:
            print('<Профилей нет. Нажмите enter>')

        print('---------------------')

        name = input('Вы выбираете профиль под номером: ')

        if name == '':  # Добавить новый профиль
            name = self.create_profile()
        else:
            name = profiles.iloc[int(name) - 1, profiles.columns.get_loc("profile_name")]

        return name
    def create_profile(self):
        profiles = pd.read_csv("profiles.csv", index_col=0)

        print('=============== Cтраница редактирования профилей ===============')

        print('----------------------------')
        print('Введите данные для заполнения информации о профиле:')
        print('----------------------------')

        a = input("Введите тип самолета ")
        b = input("Введите ФИО через пробел ")
        c = input("Введите название компании ")
        d = 0
        e = 0
        f = 0

        if input('Хотите ли вы добавить дополнительные часы налета? Y/N ') == 'Y':
            d = int(input("Введите кол-во общих часов налета: "))
            e = int(input("Введите кол-во часов дневного налета: "))
            f = int(input("Введите кол-во часов ночного налета: "))


        profiles = profiles._append({'profile_name': a,
                                          'fio': b,
                                          'company': c,
                                          'flytime_all': 0,
                                          'flytime_day': 0,
                                          'flytime_night': 0, 'add_all': d, 'add_day': e, 'add_night': f}, ignore_index=True)

        profiles.to_csv("profiles.csv", sep=',')

        return a



