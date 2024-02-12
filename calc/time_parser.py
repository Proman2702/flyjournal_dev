import pandas as pd
import datetime as dt


# Функция возвращает массив
class Calc:

    def __init__(self, profile, csv, date, period):
        self.profile = profile
        self.data = csv
        self.d = date
        self.period = period
    def make_period(self):

        self.end = list(map(int, self.d.split(' ')))
        self.end = dt.date(day=self.end[0], month=self.end[1], year=self.end[2])

        if self.period == 'd':
            self.start = self.end - dt.timedelta(days=1)

        if self.period == 'w':
            self.start = self.end - dt.timedelta(days=7)

        if self.period == 'm':
            self.start = self.end - dt.timedelta(days=30)

        if self.period == 'q':
            self.start = self.end - dt.timedelta(days=90)

        if self.period == 'y':
            self.start = self.end - dt.timedelta(days=365)

        if self.period == 'x':
            self.start = self.end - dt.timedelta(days=365*3)

        self.start = "-".join(list(map(str, [self.start.day, self.start.month, self.start.year]))[::-1])
        self.end1 = "-".join(list(map(str, [self.end.day, self.end.month, self.end.year]))[::-1])

        return self.start, self.end1

    def parser(self):
        self.data = self.data[self.data['profile'] == self.profile]

        self.data['date'] = pd.to_datetime(self.data['date'], format='%d %m %Y', dayfirst=True)


        self.data = self.data[(self.data['date'] > self.make_period()[0]) & (self.data['date'] <= self.make_period()[1])]

        return self.data


    def counter(self):

        self.csv = self.parser()

        self.csv['time_all'] = pd.to_timedelta(self.csv['time_all'])
        self.csv['time_day'] = pd.to_timedelta(self.csv['time_day'])
        self.csv['time_night'] = pd.to_timedelta(self.csv['time_night'])



        self.time_all = self.csv['time_all'].sum()
        self.daytime_all = self.csv['time_day'].sum()
        self.nighttime_all = self.csv['time_night'].sum()

        self.count = len(self.csv)


        return ([self.time_all.seconds // 3600, self.time_all.seconds // 60 % 60],
                [self.daytime_all.seconds // 3600, self.daytime_all.seconds // 60 % 60],
                [self.nighttime_all.seconds // 3600, self.nighttime_all.seconds // 60 % 60],
                self.count)


