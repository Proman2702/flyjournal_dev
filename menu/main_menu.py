import pandas as pd
import datetime
import flet as ft
import flyapp
import calc.time_parser as parser



class Main_Menu(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.app = flyapp.FlyApp()
        self.profile = open('data/current.txt').readline()  # название профиля
        self.profiles = pd.read_csv("profiles.csv")  # CSV профилей
        self.data = pd.read_csv("data.csv")  # CSV данных
        self.date = " ".join(map(str, [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]))
        self.date_vis = self.date_vision(self.date)
        self.profile_ind = self.profiles.index[self.profiles['profile_name'] == self.profile][0]  # индекс строки с инфой о профиле
        self.fio = self.profiles.at[self.profile_ind, "fio"]  # ФИО
        self.company = self.profiles.at[self.profile_ind, "company"] # компания
        self.appbar_height = 115

        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            first_date=datetime.datetime(2000, 10, 1),
            last_date=datetime.datetime.now(),
        )

        self.menubar = ft.AppBar(
            bgcolor=self.app.dark_color,
            toolbar_height=self.appbar_height,
            center_title=True,
            title=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"{' '.join(self.fio.split(' ')[0:2])}", color=self.app.dark_color, font_family='Consolas', size=21,
                                        weight=ft.FontWeight.W_400, offset=ft.Offset(-0.03, 0.0)),
                                ft.Text(f"{self.profile}", color=self.app.dark_color, font_family='Consolas', size=22,
                                        weight=ft.FontWeight.W_600),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                        bgcolor=self.app.light_color,
                        width=350,
                        height=self.appbar_height - 50,
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(30)
                    )
                ]
            ),
            actions=[]
        )

        self.pageadd = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"{self.date_vis}", size=28, weight=ft.FontWeight.W_700, color=self.app.dark_color, text_align=ft.TextAlign.CENTER),
                            width=180,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=self.app.white,
                            border_radius=30,
                            offset=ft.Offset(0.1, 0.0)
                        ),
                        ft.Container(
                            ft.Image(
                                src='https://i.imgur.com/dNiaTTh.png',
                                width=40,
                                height=40,
                                offset=ft.Offset(0.0,0.0)
                            ),
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=self.app.white,
                            border_radius=30,
                            offset=ft.Offset(0.1,0.0),
                            on_click=lambda _: self.date_picker.pick_date(),
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,offset=ft.Offset(0.0,0.5)
                ),
                ft.Container(  # ГЛАВНЫЙ КОНТЕЙНЕР
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Text('Статистика:', color=self.app.extra_color, size=23, weight=ft.FontWeight.W_500),
                                width=200,
                                height=40,
                                alignment=ft.alignment.center,
                                offset=ft.Offset(-0.45,0.1)
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.Column(
                                                    [
                                                        ft.Text('Общее время', width=105, color=self.app.dark_color, size=15, weight=ft.FontWeight.W_700),
                                                        ft.Text(f'{int((self.parsing(period="x", t="all")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_all"])}', width=80, color=self.app.extra_color, size=17, weight=ft.FontWeight.W_700),
                                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START, offset=ft.Offset(-0.05,-0.05)
                                                ),
                                                ft.Column(
                                                    [
                                                        ft.Text(f'{int((self.parsing(period="x", t="night")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_night"])}🌙', width=60, color=self.app.extra_color,size=15, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END),
                                                        ft.Text(f'{int((self.parsing(period="x", t="day")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_day"])}🔆', width=60, color=self.app.extra_color,size=15, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END),  # ЗАМЕНИТЬ
                                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END,offset=ft.Offset(0.15, -0.05)
                                                ),
                                            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        width=200,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20
                                    ),
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text('Вылетов:', width=105, color=self.app.dark_color, size=15,weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END),
                                                ft.Text(f'{self.parsing(period="x", t="count")}', width=105, color=self.app.extra_color, size=17,weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END),
                                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, offset=ft.Offset(-0.15,-0.05)
                                        ),
                                        width=100,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20

                                    )
                                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),

                            ft.Row(
                                [
                                    ft.Text("За день:", size=16, color=self.app.light_color, width=70, height=30, weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05,0.0)
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.Column(
                                                    [
                                                        ft.Text('Всего:', width=60, color=self.app.dark_color,
                                                                size=15, weight=ft.FontWeight.W_700),
                                                        ft.Text(f'{self.parsing("d", t="night")}🌙 {self.parsing("d", t="day")}🔆', width=95, color=self.app.dark_color,
                                                                size=13, weight=ft.FontWeight.W_700),
                                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    offset=ft.Offset(-0.05, -0.05)
                                                ),
                                                ft.Column(
                                                    [
                                                        ft.Text(f'{self.parsing(period="d", t="count")} вылет{self.word_ending(num=self.parsing(period="d", t="count"))}', width=80, color=self.app.extra_color, size=15,
                                                                weight=ft.FontWeight.W_700,
                                                                text_align=ft.TextAlign.END),
                                                        ft.Text(f'{self.float_time(self.parsing(period="d", t="all"))} часов', width=80, color=self.app.extra_color, size=15,
                                                                weight=ft.FontWeight.W_700,
                                                                text_align=ft.TextAlign.END),  # ЗАМЕНИТЬ
                                                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                                    offset=ft.Offset(0.0, -0.05)
                                                ),
                                            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        width=200,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,

                                    ),
                                    ft.Container(
                                        ft.Column(
                                            [

                                            ]
                                        ),
                                        width=100,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                        )

                                    )

                                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),

                            ft.Row(
                                [
                                    ft.Text("За остальное время:", size=16, color=self.app.light_color, width=170, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=120, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text('За неделю:', width=100, color=self.app.dark_color,
                                                                size=15, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.START),
                                                ft.Row(
                                                    [
                                                        ft.Text(f'{self.float_time(self.parsing("w", t="all"))} ч.:', width=80, color=self.app.extra_color,
                                                                size=14, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.START),
                                                        ft.Text(f'{self.float_time(self.parsing("w", t="night"))}🌙 {self.float_time(self.parsing("w", t="day"))}🔆', width=100, color=self.app.dark_color,
                                                                size=12, weight=ft.FontWeight.W_700, offset=ft.Offset(-0.48,0.0), text_align=ft.TextAlign.END),
                                                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Text(f'{self.parsing(period="w", t="count")} вылет{self.word_ending(num=self.parsing(period="w", t="count"))}', width=100, color=self.app.extra_color,
                                                                size=14, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.START)
                                                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.START,
                                                offset=ft.Offset(0.05, -0.05),
                                        ),
                                        width=152,
                                        height=100,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,

                                    ),
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text('За месяц:', width=100, color=self.app.dark_color,
                                                        size=15, weight=ft.FontWeight.W_700,
                                                        text_align=ft.TextAlign.START),
                                                ft.Row(
                                                    [
                                                        ft.Text(f'{self.parsing("m", t="all").split(":")[0]} ч.:', width=80, color=self.app.extra_color,
                                                                size=14, weight=ft.FontWeight.W_700,
                                                                text_align=ft.TextAlign.START),
                                                        ft.Text(f'{self.parsing("m", t="night").split(":")[0]}🌙 {self.parsing("m", t="day").split(":")[0]}🔆', width=100, color=self.app.dark_color,
                                                                size=13, weight=ft.FontWeight.W_700,
                                                                offset=ft.Offset(-0.48, 0.0),
                                                                text_align=ft.TextAlign.END),
                                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Text(f'{self.parsing(period="m", t="count")} вылет{self.word_ending(num=self.parsing(period="m", t="count"))}', width=100, color=self.app.extra_color,
                                                        size=14, weight=ft.FontWeight.W_700,
                                                        text_align=ft.TextAlign.START)
                                            ], spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                            offset=ft.Offset(0.05, -0.05),
                                        ),
                                        width=152,
                                        height=100,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,

                                    ),

                                ], spacing=18, alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text('За квартал:', width=100, color=self.app.dark_color,
                                                        size=15, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.START),
                                                ft.Row(
                                                    [
                                                        ft.Text(f'{self.parsing("q", t="all").split(":")[0]} ч.:', width=80, color=self.app.extra_color,
                                                                size=14, weight=ft.FontWeight.W_700,
                                                                text_align=ft.TextAlign.START),
                                                        ft.Text(f'{self.parsing("q", t="night").split(":")[0]}🌙 {self.parsing("q", t="day").split(":")[0]}🔆', width=100, color=self.app.dark_color,
                                                                size=13, weight=ft.FontWeight.W_700,
                                                                offset=ft.Offset(-0.48, 0.0), text_align=ft.TextAlign.END),
                                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Text(f'{self.parsing(period="q", t="count")} вылет{self.word_ending(num=self.parsing(period="q", t="count"))}', width=100, color=self.app.extra_color,
                                                        size=14, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.START)
                                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                            offset=ft.Offset(0.05, -0.05),
                                        ),
                                        width=152,
                                        height=100,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,

                                    ),
                                    ft.Container(
                                        ft.Column(
                                            [
                                                ft.Text('За год:', width=100, color=self.app.dark_color,
                                                        size=15, weight=ft.FontWeight.W_700,
                                                        text_align=ft.TextAlign.START),
                                                ft.Row(
                                                    [
                                                        ft.Text(f'{self.parsing("y", t="all").split(":")[0]} ч.:', width=80, color=self.app.extra_color,
                                                                size=14, weight=ft.FontWeight.W_700,
                                                                text_align=ft.TextAlign.START),
                                                        ft.Text(f'{self.parsing("y", t="night").split(":")[0]}🌙 {self.parsing("y", t="day").split(":")[0]}🔆', width=100, color=self.app.dark_color,
                                                                size=13, weight=ft.FontWeight.W_700,
                                                                offset=ft.Offset(-0.48, 0.0),
                                                                text_align=ft.TextAlign.END),
                                                    ], alignment=ft.MainAxisAlignment.CENTER,
                                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                                ),
                                                ft.Text(f'{self.parsing(period="y", t="count")} вылет{self.word_ending(num=self.parsing(period="y", t="count"))}', width=100, color=self.app.extra_color,
                                                        size=14, weight=ft.FontWeight.W_700,
                                                        text_align=ft.TextAlign.START)
                                            ], spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                            offset=ft.Offset(0.05, -0.05),
                                        ),
                                        width=152,
                                        height=100,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,

                                    ),

                                ], spacing=18, alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=ft.Offset(0.0,0.1)
                            ),

                            ft.Container(
                                content=ft.Text('Информация:', color=self.app.extra_color, size=23,
                                                weight=ft.FontWeight.W_500),
                                width=200,
                                height=50,
                                alignment=ft.alignment.center,
                                offset=ft.Offset(-0.4, 0.0)
                            ),

                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text("Авиакомпания", color=self.app.dark_color, size=14, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER, offset=ft.Offset(-0.03,-0.2)),
                                                ft.Text(f"{self.company}", color=self.app.extra_color, size=17,
                                                        weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END, offset=ft.Offset(-0.03,0.0)),
                                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5, offset=ft.Offset(-0.1,-0.05)
                                        ),
                                        width=130,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text("ФИО", color=self.app.dark_color, size=14, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.START, offset=ft.Offset(-0.1, 0.1), width=145),
                                                ft.Text(f"{''.join(self.fio.split(' ')[0:1])}", color=self.app.extra_color, size=14,
                                                        weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END, offset=ft.Offset(-0.03,0.2), width=150),
                                                ft.Text(f"{' '.join(self.fio.split(' ')[1:3])}", color=self.app.extra_color, size=14,
                                                        weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END,
                                                        offset=ft.Offset(-0.03, 0.2), width=180)
                                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0, offset=ft.Offset(-0.05,-0.05)
                                        ),
                                        width=178,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20
                                    )
                                ], spacing=12, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text("Судно", color=self.app.dark_color, size=14,
                                                        weight=ft.FontWeight.W_600, text_align=ft.TextAlign.START,
                                                        offset=ft.Offset(-0.03, -0.2), width=170),
                                                ft.Text(f"{self.profile}", color=self.app.extra_color, size=20,
                                                        weight=ft.FontWeight.W_700, text_align=ft.TextAlign.END,
                                                        offset=ft.Offset(0.0, 0.05)),
                                            ], alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.END, spacing=5,
                                            offset=ft.Offset(-0.1, -0.05)
                                        ),
                                        width=205,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [

                                            ]
                                        ),
                                        width=100,
                                        height=80,
                                        bgcolor=self.app.light_color,
                                        border_radius=20,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                        )
                                    )
                                ], spacing=15, alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=ft.Offset(0.0,0.1)
                            )
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        offset=ft.Offset(0.0, 0.005),

                    ),
                    bgcolor=self.app.white,
                    width=350,
                    height=770,
                    border_radius=30

                )
            ],
            spacing=100,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

    # перезапись даты
    def date_vision(self, t):
        d = t.split(" ")[0]
        m = t.split(" ")[1]
        y = t.split(" ")[2]

        if len(d) == 1:
            d = "0" + d
        if len(m) == 1:
            m = "0" + m

        return f"{d}.{m}.{y}"

    # парсер данных
    def parsing(self, period, t):
        result = 0
        if t == 'all':
            result = parser.Calc(profile=self.profile,csv=self.data, date=self.date, period=period).counter()[0]

            if str(result[1]) == '0':
                result[1] = '00'
            result = ':'.join(list(map(str, [result[0], result[1]])))
            #if period == 'x':
                #print(f'ОБЩЕЕ ВРЕМЯ {result}')
        if t == 'day':
            result = parser.Calc(profile=self.profile,csv=self.data, date=self.date, period=period).counter()[1]
            if str(result[1]) == '0':
                result[1] = '00'
            result = ':'.join(list(map(str, [result[0], result[1]])))
        if t == 'night':
            result = parser.Calc(profile=self.profile,csv=self.data, date=self.date, period=period).counter()[2]
            if str(result[1]) == '0':
                result[1] = '00'
            result = ':'.join(list(map(str, [result[0], result[1]])))
        if t == 'count':
            result = parser.Calc(profile=self.profile,csv=self.data, date=self.date, period=period).counter()[3]
        return result

    # изменение окончаний
    def word_ending(self, num):
        num = int(num)
        if 10 <= num % 100 <= 19:
            return 'ов'
        elif num % 10 == 1:
            return ''
        elif 2 <= num % 10 <= 4:
            return 'а'
        else:
            return 'ов'

    # перевод времени в float
    def float_time(self, t):
        h = float(t.split(":")[0])
        m = float(t.split(":")[1])

        m = m / 60

        return f'{h+m:.1f}'

    # при смене даты
    def change_date(self, e):
        # page.add.controls[1].controls[...] - ряды главного контейнера
        self.main_container = self.pageadd.controls[1].content.controls
        # page.add.controls[1].controls[...].controls[0/1].content - левый/правый контейнер
        self.date = " ".join(map(str, [self.date_picker.value.day, self.date_picker.value.month, self.date_picker.value.year]))
        self.date_vis = self.date_vision(self.date)
        self.pageadd.controls[0].controls[0].content.value = self.date_vis

        #Контейнер с общим временем
        self.main_container[1].controls[0].content.controls[0].controls[1].value = f'{int((self.parsing(period="x", t="all")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_all"])}' # всего общего времени
        self.main_container[1].controls[0].content.controls[1].controls[0].value = f'{int((self.parsing(period="x", t="night")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_night"])}🌙' # всего ночного времени
        self.main_container[1].controls[0].content.controls[1].controls[1].value = f'{int((self.parsing(period="x", t="day")).split(":")[0])+int(self.profiles.at[self.profile_ind, "add_day"])}🔆' # всего дневного времени
        # Контейнер с общими полетами
        self.main_container[1].controls[1].content.controls[1].value = f'{self.parsing(period="x", t="count")}' # всего полетов
        # Контейнер с дневными данными
        self.main_container[3].controls[0].content.controls[0].controls[1].value = f'{self.parsing("d", t="night")}🌙 {self.parsing("d", t="day")}🔆'  # всего общего времени
        self.main_container[3].controls[0].content.controls[1].controls[0].value = f'{self.parsing(period="d", t="count")} вылет{self.word_ending(num=self.parsing(period="d", t="count"))}'
        self.main_container[3].controls[0].content.controls[1].controls[1].value = f'{self.float_time(self.parsing(period="d", t="all"))} часов'
        # Контейнер с недельными данными
        self.main_container[5].controls[0].content.controls[1].controls[0].value = f'{self.float_time(self.parsing("w", t="all"))} ч.:'  #
        self.main_container[5].controls[0].content.controls[1].controls[1].value = f'{self.float_time(self.parsing("w", t="night"))}🌙 {self.float_time(self.parsing("w", t="day"))}🔆'  #
        self.main_container[5].controls[0].content.controls[2].value = f'{self.parsing(period="w", t="count")} вылет{self.word_ending(num=self.parsing(period="w", t="count"))}'  #
        # Контейнер с месячными данными
        self.main_container[5].controls[1].content.controls[1].controls[0].value = f'{self.parsing("m", t="all").split(":")[0]} ч.:'  #
        self.main_container[5].controls[1].content.controls[1].controls[1].value = f'{self.parsing("m", t="night").split(":")[0]}🌙 {self.parsing("m", t="day").split(":")[0]}🔆'  #
        self.main_container[5].controls[1].content.controls[2].value = f'{self.parsing(period="m", t="count")} вылет{self.word_ending(num=self.parsing(period="m", t="count"))}'  #
        # Контайнер с квартальными данными
        self.main_container[6].controls[0].content.controls[1].controls[
            0].value = f'{self.parsing("q", t="all").split(":")[0]} ч.:'  #
        self.main_container[6].controls[0].content.controls[1].controls[
            1].value = f'{self.parsing("q", t="night").split(":")[0]}🌙 {self.parsing("q", t="day").split(":")[0]}🔆'  #
        self.main_container[6].controls[0].content.controls[
            2].value = f'{self.parsing(period="q", t="count")} вылет{self.word_ending(num=self.parsing(period="q", t="count"))}'  #
        # Контейнер с годовыми данными
        self.main_container[6].controls[1].content.controls[1].controls[
            0].value = f'{self.parsing("y", t="all").split(":")[0]} ч.:'  #
        self.main_container[6].controls[1].content.controls[1].controls[
            1].value = f'{self.parsing("y", t="night").split(":")[0]}🌙 {self.parsing("y", t="day").split(":")[0]}🔆'  #
        self.main_container[6].controls[1].content.controls[
            2].value = f'{self.parsing(period="y", t="count")} вылет{self.word_ending(num=self.parsing(period="y", t="count"))}'  #

        self.pageadd.update()
        self.page.update()

    def build(self):
        return self.pageadd


