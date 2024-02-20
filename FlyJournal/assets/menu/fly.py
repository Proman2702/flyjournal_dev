import pandas as pd
import flet as ft
import datetime
from assets import flyapp
import assets.calc.data_parser
import assets.calc.fly_time

class Fly_Menu(ft.UserControl):
    def __init__(self):
        self.last = 0
        super().__init__()
        self.app = flyapp.FlyApp()
        self.data = pd.read_csv('assets/data.csv')
        self.profiles = pd.read_csv('assets/profiles.csv')
        self.profile = open('assets/data/current.txt').readline()
        self.code = open('assets/data/airport.txt').readline()
        self.date = " ".join(map(str, [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]))
        self.date_vis = self.date_vision(self.date)
        self.calc = assets.calc.fly_time.TimeCalculation()

        self.date_picker = ft.DatePicker(on_change=self.change_date,first_date=datetime.datetime(2000, 1, 1),last_date=datetime.datetime.now())

        self.bs = ft.BottomSheet(open=False)  # всплывающие окна
        self.fill_fields()
        self.fill_title = ft.Row(
                [
                    ft.Text('Полет №1', color=self.app.dark_color, size=20, weight=ft.FontWeight.W_700, offset=ft.Offset(-0.3,0.0)),
                    ft.Container(
                        ft.Image(
                            src='assets/img/green.png',
                            width=30,
                            height=30
                        ),
                        width=30,
                        height=30,
                        border_radius=1,
                        on_click=self.add_flight
                    ),
                    ft.Container(
                        ft.Image(
                            src='assets/img/yellow.png',
                            width=30,
                            height=30
                        ),
                        width=30,
                        border_radius=1,
                        height=30,
                        on_click=self.save_to_buffer
                    ),
                    ft.Container(
                        ft.Image(
                            src='assets/img/red.png',
                            width=30,
                            height=30,
                            fit=ft.ImageFit.FILL
                        ),
                        width=30,
                        height=30,
                        border_radius=1,
                        on_click=self.del_flight
                    )
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                offset=ft.Offset(0.05,0.0)
            )

        self.fill_menu = ft.AlertDialog(
            actions=[
                ft.ListView(
                    controls=[
                        ft.Row([ft.Text("Номер самолета", color=self.app.dark_color, size=14, weight=ft.FontWeight.W_600,width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.plane], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Номер      рейса", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.way], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Отправление из аэропорта", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.departure_place], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Прибытие в аэропорт", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.arrival_place], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Checkbox(on_change=self.hide1,label="", value=False,scale=0.7, offset=ft.Offset(-0.2,0)),ft.Text('На запасной', color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=68, height=50, offset=ft.Offset(-0.1, 0.1)),self.arrival_place2], offset=ft.Offset(-0.07,0.0), spacing=0, alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Row([ft.Text("Время    запуска", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_on], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Время выключения", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_off], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Время     взлета", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_dep], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Время посадки", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_arr], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Checkbox(on_change=self.hide2,label="", value=False,scale=0.7, offset=ft.Offset(-0.2,0.6)),ft.Text("Время    PVP", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=68, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_PVP], spacing=0, alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=ft.Offset(-0.07,0.0)),
                        ft.Row([ft.Checkbox(on_change=self.hide2,label="", value=False,scale=0.0, offset=ft.Offset(-0.2,0.6)),ft.Text("Время    PPP", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=68, height=50, offset=ft.Offset(-0.1, 0.1)),self.time_PPP], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=ft.Offset(-0.07,0.0), spacing=0),
                        ft.Row([ft.Text("Запланированный взлет", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.etd], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Запланированная посадка", color=self.app.dark_color, size=14,weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),self.eta], alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Общее время полета", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),
                                self.vis_all_time], alignment=ft.MainAxisAlignment.CENTER,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Время в воздухе", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),
                                self.vis_fly_time],
                               alignment=ft.MainAxisAlignment.CENTER,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                        ft.Row([ft.Text("Расчетное время", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_600, width=100, height=50, offset=ft.Offset(-0.1, 0.1)),
                                self.vis_est_time],
                               alignment=ft.MainAxisAlignment.CENTER,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    ],
                    height=250,
                    divider_thickness=30,
                    spacing=0,
                    padding=ft.padding.symmetric(horizontal=40)
                )
            ], inset_padding=ft.padding.symmetric(vertical=60, horizontal=2),
            title=self.fill_title,
            title_padding=ft.padding.symmetric(vertical=10, horizontal=60)
        )

        self.pageadd = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"{self.date_vis}", size=28, weight=ft.FontWeight.W_700,
                                            color=self.app.dark_color, text_align=ft.TextAlign.CENTER),
                            width=180,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=self.app.white,
                            border_radius=30,
                            offset=ft.Offset(0.1, 0.0)
                        ),
                        ft.Container(
                            ft.Image(
                                src='assets/img/calendar.png',
                                width=40,
                                height=40,
                                offset=ft.Offset(0.0, 0.0)
                            ),
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=self.app.white,
                            border_radius=30,
                            offset=ft.Offset(0.1, 0.0),
                            on_click=lambda _: self.date_picker.pick_date(),
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0, offset=ft.Offset(0.0, 0.5)
                ),

                ft.Container(  # ГЛАВНЫЙ КОНТЕЙНЕР
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("1 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(  # 1 полет
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                on_click=self.f1
                            ),
                            ft.Row(
                                [
                                    ft.Text("2 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(  # 2 полет
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                on_click=self.f2
                            ),
                            ft.Row(
                                [
                                    ft.Text("3 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(  # 3 полет
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                on_click=self.f3
                            ),
                            ft.Row(
                                [
                                    ft.Text("4 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(  # 4 полет
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                on_click=self.f4
                            ),
                            ft.Row(
                                [
                                    ft.Text("5 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(  # 5 полет
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center,
                                on_click=self.f5
                            )
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        offset=ft.Offset(0.0, 0.005),

                    ),
                    bgcolor=self.app.white,
                    width=350,
                    height=580,
                    border_radius=30

                )
            ],
            spacing=100,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.visual()

    def build(self):
        return self.pageadd

    # Заполнение самих полей ввода
    def visual(self):
        for i in range(1, 6):
            if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(i), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
                data = assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(i), date=self.date, mode='get', profile=self.profile).main()[1]
                print(data["place_departure"].iat[0])
                self.pageadd.controls[1].content.controls[i * 2 - 1].content = ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(f'{data["place_departure"].iat[0]}', height=30, size=20, weight=ft.FontWeight.W_700, color=self.app.dark_color),
                                ft.Text(f'{data["time_on"].iat[0]}', height=30, size=18, weight=ft.FontWeight.W_600, color=self.app.dark_color)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=-30
                        ),
                        ft.Column(
                            [
                                ft.Image(
                                    src='assets/img/duga1.png',
                                    width=180
                                ),
                                ft.Row(
                                    [
                                        ft.Text(f'🛬{(data["time_all"].iat[0])[:-3]}', height=30, size=15,
                                                weight=ft.FontWeight.W_500,
                                                color=self.app.dark_color)
                                    ]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=-30,
                            offset=ft.Offset(0.0,0.1)
                        ),
                        ft.Column(
                            [
                                ft.Text(f'{data["place_arrival"].iat[0]}', height=30, size=20, weight=ft.FontWeight.W_700,
                                        color=self.app.dark_color),
                                ft.Text(f'{data["time_off"].iat[0]}', height=30, size=18, weight=ft.FontWeight.W_600,
                                        color=self.app.dark_color)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=-30
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                )
            elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(i), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
                self.pageadd.controls[1].content.controls[i * 2 - 1].content = ft.Text("В буфере", color=self.app.extra_color, size=16, weight=ft.FontWeight.W_800
                )
            else:
                self.pageadd.controls[1].content.controls[i*2-1].content = ft.Image(
                                                    src='assets/img/blue_plus.png',
                                                    width=40,
                                                    height=40
                                                )

    # Скрытие запасного
    def hide1(self, e):
        if self.arrival_place2.disabled:
            self.arrival_place2.disabled = False
            self.arrival_place2.bgcolor = self.app.white

            self.arrival_place.disabled = True
            self.arrival_place.bgcolor = self.app.grey
            self.arrival_place.value = ''
        else:
            self.arrival_place2.disabled = True
            self.arrival_place2.bgcolor = self.app.grey
            self.arrival_place2.value = ''

            self.arrival_place.disabled = False
            self.arrival_place.bgcolor = self.app.white
        self.fill_menu.update()

    # Скрытие PVP/PPP
    def hide2(self, e):
        if self.time_PVP.disabled:
            self.time_PVP.disabled = False
            self.time_PVP.bgcolor = self.app.white
            self.time_PPP.disabled = False
            self.time_PPP.bgcolor = self.app.white
        else:
            self.time_PVP.disabled = True
            self.time_PPP.disabled = True
            self.time_PVP.value = ''
            self.time_PPP.value = ''
            self.time_PVP.bgcolor = self.app.grey
            self.time_PPP.bgcolor = self.app.grey
        self.fill_menu.update()

    # 1 ячейка
    def f1(self, e):
        self.fill_title.controls[0].value = 'Полет №1'
        self.fill_title.controls[1].border_radius = 1
        self.fill_title.controls[2].border_radius = 1
        self.fill_title.controls[3].border_radius = 1
        self.fill_menu.title = self.fill_title
        self.fill_menu.open = True
        if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(1), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
            self.set_up('all', '1')
        elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(1), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
            self.set_up('buffer', '1')
        else:
            self.set_up('none', '1')

        self.fill_menu.update()

    # 2 ячейка
    def f2(self, e):
        self.fill_title.controls[0].value = 'Полет №2'
        self.fill_title.controls[1].border_radius = 2
        self.fill_title.controls[2].border_radius = 2
        self.fill_title.controls[3].border_radius = 2
        self.fill_menu.title = self.fill_title
        self.fill_menu.open = True
        if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(2), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
            self.set_up('all', '2')
        elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(2), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
            self.set_up('buffer', '2')
        else:
            self.set_up('none', '2')

        self.fill_menu.update()

    # 3 ячейка
    def f3(self, e):
        self.fill_title.controls[0].value = 'Полет №3'
        self.fill_title.controls[1].border_radius = 3
        self.fill_title.controls[2].border_radius = 3
        self.fill_title.controls[3].border_radius = 3
        self.fill_menu.title = self.fill_title
        self.fill_menu.open = True
        if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(3), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
            self.set_up('all', '3')
        elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(3), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
            self.set_up('buffer', '3')
        else:
            self.set_up('none', '3')

        self.fill_menu.update()

    # 4 ячейка
    def f4(self, e):

        self.fill_title.controls[0].value = 'Полет №4'
        self.fill_title.controls[1].border_radius = 4
        self.fill_title.controls[2].border_radius = 4
        self.fill_title.controls[3].border_radius = 4
        self.fill_menu.title = self.fill_title
        self.fill_menu.open = True
        if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(4), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
            self.set_up('all', '4')
        elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(4), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
            self.set_up('buffer', '4')
        else:
            self.set_up('none', '4')

        self.fill_menu.update()

    # 5 ячейка
    def f5(self, e):
        self.fill_title.controls[0].value = 'Полет №5'
        self.fill_title.controls[1].border_radius = 5
        self.fill_title.controls[2].border_radius = 5
        self.fill_title.controls[3].border_radius = 5
        self.fill_menu.title = self.fill_title
        self.fill_menu.open = True
        if assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(5), date=self.date, mode='get', profile=self.profile).main()[0] == 1:
            self.set_up('all', '5')
        elif assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(5), date=self.date, mode='get', profile=self.profile).main()[0] == 2:
            self.set_up('buffer', '5')
        else:
            self.set_up('none', '5')
        self.fill_menu.update()

    # заполнение и наименования полей
    def fill_fields(self):
        # номер самолета
        self.plane = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                  border_color=self.app.light_color, content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0),
                                  disabled=False, value='')
        # номер рейса
        self.way = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                border_color=self.app.light_color, content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0),
                                disabled=False, value='')
        # вылет
        self.departure_place = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                            border_color=self.app.light_color,
                                            content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False, value='', capitalization=ft.TextCapitalization.CHARACTERS)
        # прибытие
        self.arrival_place = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                          border_color=self.app.light_color,
                                          content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False, value='', capitalization=ft.TextCapitalization.CHARACTERS)
        # запасной (неактивный/активный)
        self.arrival_place2 = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.grey,
                                           border_color=self.app.light_color,
                                           content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='', capitalization=ft.TextCapitalization.CHARACTERS)
        # время от (для расчета)
        self.time_on = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                     border_color=self.app.light_color,
                                     content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False, value='', on_change=self.format_input)
        # время до (для расчета)
        self.time_off = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                     border_color=self.app.light_color,
                                     content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False, value='', on_change=self.format_input)
        # время отрыва колес
        self.time_dep = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                    border_color=self.app.light_color, content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0),
                                    disabled=False, value='', on_change=self.format_input)
        # время приземления
        self.time_arr = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                     border_color=self.app.light_color,
                                     content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False, value='', on_change=self.format_input)
        # время (неактивный/активный)
        self.time_PVP = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.grey,
                                     border_color=self.app.light_color,
                                     content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='', on_change=self.format_input)
        # время (неактивный/активный)
        self.time_PPP = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.grey,
                                     border_color=self.app.light_color,
                                     content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='', on_change=self.format_input)
        # время запланированного взлета
        self.etd = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                border_color=self.app.light_color, content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0),
                                disabled=False, value='', on_change=self.format_input)
        # время запланированной посадки
        self.eta = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white,
                                border_color=self.app.light_color, content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0),
                                disabled=False, value='', on_change=self.format_input)
        # время общего полета
        self.vis_all_time = ft.Text("<Не рассчитано>", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_800, width=130, height=50, offset=ft.Offset(0.0, 0.1))
        # время в воздухе
        self.vis_fly_time = ft.Text("<Не рассчитано>", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_800, width=130, height=50, offset=ft.Offset(0.0, 0.1))
        # время запланированное
        self.vis_est_time = ft.Text("<Не рассчитано>", color=self.app.dark_color, size=14,
                                        weight=ft.FontWeight.W_800, width=130, height=50, offset=ft.Offset(0.0, 0.1))

    # заполнение полей при заходе в ячейку
    def set_up(self, fill, num):

        if fill == 'buffer':
            print('entered buffer')
            data = assets.calc.data_parser.Parsing(mode='get', big_data=self.data, date=self.date, data='', num=str(num),
                                                   profile=self.profile).main()[1]
            self.plane.value = data['plane_number'].iat[0]
            self.way.value = data['flight'].iat[0]
            self.departure_place.value = data['place_departure'].iat[0]
            self.arrival_place.value = data['place_arrival'].iat[0]
            self.arrival_place2.value = data['place_arrival2'].iat[0]
            self.time_on.value = data['time_on'].iat[0]
            self.time_off.value = data['time_off'].iat[0]
            self.time_dep.value = data['time_departure'].iat[0]
            self.time_arr.value = data['time_arrival'].iat[0]
            self.time_PVP.value = data['time_PVP'].iat[0]
            self.time_PPP.value = data['time_PPP'].iat[0]
            self.etd.value = data['ETD'].iat[0]
            self.eta.value = data['ETA'].iat[0]
            self.vis_est_time.value = '<Не рассчитано>'
            self.vis_all_time.value = '<Не рассчитано>'
            self.vis_fly_time.value = '<Не рассчитано>'

        if fill == 'all':
            data = assets.calc.data_parser.Parsing(mode='get', big_data=self.data, date=self.date, data='', num=str(num),
                                                   profile=self.profile).main()[1]
            print(data['time_all'])
            print('entered all')
            self.plane.value = data['plane_number'].iat[0]
            self.way.value = data['flight'].iat[0]
            self.departure_place.value = data['place_departure'].iat[0]
            self.arrival_place.value = data['place_arrival'].iat[0]
            self.arrival_place2.value = data['place_arrival2'].iat[0]
            self.time_on.value = data['time_on'].iat[0]
            self.time_off.value = data['time_off'].iat[0]
            self.time_dep.value = data['time_departure'].iat[0]
            self.time_arr.value = data['time_arrival'].iat[0]
            self.time_PVP.value = data['time_PVP'].iat[0]
            self.time_PPP.value = data['time_PPP'].iat[0]
            self.etd.value = data['ETD'].iat[0]
            self.eta.value = data['ETA'].iat[0]
            self.vis_all_time.value = data['time_all'].iat[0]
            self.vis_fly_time.value = data['time_air'].iat[0]
            self.vis_est_time.value = data['ETD_ETA_all'].iat[0]

        if fill == 'none':
            self.plane.value = ''
            self.way.value = ''
            self.departure_place.value = ''
            self.arrival_place.value = ''
            self.arrival_place2.value = ''
            self.time_on.value = ''
            self.time_off.value = ''
            self.time_dep.value = ''
            self.time_arr.value = ''
            self.time_PVP.value = ''
            self.time_PPP.value = ''
            self.etd.value = ''
            self.eta.value = ''
            self.vis_est_time.value = '<Не рассчитано>'
            self.vis_all_time.value = '<Не рассчитано>'
            self.vis_fly_time.value = '<Не рассчитано>'

    def format_input(self, e):
        if len(e.control.value) == 1:
            self.last = 1
        if len(e.control.value) == 2 and self.last == 2:
            e.control.value += ' '
            self.fill_menu.update()
        self.last += 1




    # просто закрыть всплывающее окно
    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    # закрыть всплывающее окно с удалением данных
    def close_bs_delete(self, e):
        self.data = assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(n), date=self.date, mode="delete",
                                                    profile=self.profile).main()[1]
        self.visual()
        self.pageadd.update()
        self.fill_menu.open = False
        self.fill_menu.update()

        self.bs.open = False
        self.bs.update()

    # форматирование даты для визуала
    def date_vision(self, t):
        d = t.split(" ")[0]
        m = t.split(" ")[1]
        y = t.split(" ")[2]

        if len(d) == 1:
            d = "0" + d
        if len(m) == 1:
            m = "0" + m

        return f"{d}.{m}.{y}"

    # форматирование времени для визуала
    def time_vision(self, t):
        h = t.split(" ")[0]
        m = t.split(" ")[1]
        s = '00'

        if len(h) == 1:
            h = "0" + h
        if len(m) == 1:
            m = "0" + m

        return f"{h}:{m}:{s}"

    # сохранение в буфер (желтая кнопка)
    def save_to_buffer(self, e):
        num = str(e.control.border_radius)

        data_filled = {"profile": self.profile,  # профиль
                       "date": self.date,  # дата
                       "number": str(num),  # номер (в день до 5)
                       "plane_number": self.plane.value,  # номер самолета
                       "flight": self.way.value,  # номер рейса
                       "place_departure": self.departure_place.value,  # место отправления
                       "place_arrival": self.arrival_place.value,  # место прибытия
                       "place_arrival2": self.arrival_place2.value,  # запасной (неактивный/активный)
                       "time_on": self.time_on.value,  # время включения двигателей (ДЛЯ РАСЧЕТА)
                       "time_off": self.time_off.value,  # время выключения двигателей (ДЛЯ РАСЧЕТА)
                       "time_departure": self.time_dep.value,  # время отрыва колес
                       "time_arrival": self.time_arr.value,  # время приземления
                       "time_PVP": self.time_PVP.value,  # время (неактивный/активный)
                       "time_PPP": self.time_PPP.value,  # время (неактивный/активный)
                       "ETD": self.etd.value,  # во сколько должны были взлететь
                       "ETA": self.eta.value,  # во сколько должны были сесть
                       "time_all": '',  # общее время от вкл до выкл (ДЛЯ РАСЧЕТА)
                       "time_air": '',  # общее время в воздухе
                       "time_day": '',  # от общего времени
                       "time_night": '',  # от общего времени
                       "time_PVP_PPP_all": '',  # ничего нет
                       "ETD_ETA_all": ''}  # суммирование etd + eta
        assets.calc.data_parser.Parsing(big_data=self.data, data=data_filled, num=str(num), date=self.date, mode='delay',
                                        profile=self.profile).main()
        self.bs.content = ft.Container(ft.Column([
            ft.Text("Данные сохранены в буфер обмена!"),
            ft.ElevatedButton("Закрыть", on_click=self.close_bs),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        self.visual()
        self.pageadd.update()
        self.fill_menu.open = False
        self.fill_menu.update()

        self.bs.open = False
        self.bs.update()



    # удалить полет (красная кнопка)
    def del_flight(self, e):

        num = str(e.control.border_radius)
        print(num)
        d = ''

        def error_handler(t):
            if t == 'not_found':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, полета не существует"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)

        d = assets.calc.data_parser.Parsing(big_data=self.data, data='', num=str(num), date=self.date, mode='get',
                                            profile=self.profile).main()[0]

        if d == 0 or d == 2:
            error_handler('not_found')
            self.bs.open = True
            self.bs.update()
        else:
            global n
            n = num
            self.bs.content = ft.Container(ft.Column([
                ft.Text("Вы точно хотите удалить данные?"),
                ft.ElevatedButton("Удалить", on_click=self.close_bs_delete),
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            self.bs.open = True
            self.bs.update()

    # сохранить полет (зеленая кнопка)
    def add_flight(self, e):
        error = False
        num = str(e.control.border_radius)

        def error_handler(t):
            if t == 'not_filled':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, некоторые поля не заполнены"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)

            if t == 'format':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, введенный текст не соответствует формату"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)

            if t == 'not_found':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, введенный аэропорт не найден"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            self.bs.open = True
            self.page.update()

        if self.plane.value == '' or self.way.value == '' or self.departure_place.value == '' or (not self.arrival_place.disabled and self.arrival_place.value == '') or (not self.arrival_place2.disabled and self.arrival_place2.value == '') or self.time_dep.value == '' or self.time_arr.value == '' or self.time_on.value == '' or self.time_off.value == '' or self.etd.value == '' or self.eta.value == '':
            error = True
            error_handler('not_filled')
            print("fill error")

        if not error:

            try:
                # ---------------------------
                t_d_air = self.calc.time_rewrite(self.time_dep.value, False)
                t_a_air = self.calc.time_rewrite(self.time_arr.value, False)

                etd = self.calc.time_rewrite(self.etd.value, False)
                eta = self.calc.time_rewrite(self.eta.value, False)

                t_air = ' '.join([str(self.calc.time_summary(t_d_air, t_a_air).seconds // 3600),
                                  str(self.calc.time_summary(t_d_air, t_a_air).seconds // 60 % 60)])
                t_air = self.time_vision(t_air)

                etd_eta = ' '.join([str(self.calc.time_summary(etd, eta).seconds // 3600),
                                    str(self.calc.time_summary(etd, eta).seconds // 60 % 60)])
                etd_eta = self.time_vision(etd_eta)
                print('processed after time_sum')
                # ---------------------------
                if self.arrival_place.disabled:
                    time_calc = assets.calc.fly_time.TimeResult(self.departure_place.value,
                                                                self.arrival_place2.value,
                                                                d=self.time_on.value,
                                                                a=self.time_off.value, date=self.date, code=self.code)
                else:
                    time_calc = assets.calc.fly_time.TimeResult(self.departure_place.value,
                                                                self.arrival_place.value,
                                                                d=self.time_on.value,
                                                                a=self.time_off.value, date=self.date, code=self.code)

                print('processed after class')

                time_all = " ".join([str(time_calc.all_time.seconds // 3600), str(time_calc.all_time.seconds // 60 % 60)])
                time_day = time_calc.time_logic()[1]
                time_night = time_calc.time_logic()[0]

                print('processed after getting')

                time_day = " ".join([str(time_day.seconds // 3600), str(time_day.seconds // 60 % 60)])
                time_night = " ".join([str(time_night.seconds // 3600), str(time_night.seconds // 60 % 60)])

                print('processed after formatting')

                time_all = self.time_vision(time_all)
                time_day = self.time_vision(time_day)
                time_night = self.time_vision(time_night)

                print(time_all, time_day, time_night)

                data_filled = {"profile": self.profile,  # профиль
                               "date": self.date,  # дата
                               "number": str(num),  # номер (в день до 5)
                               "plane_number": self.plane.value,  # номер самолета
                               "flight": self.way.value,  # номер рейса
                               "place_departure": self.departure_place.value,  # место отправления
                               "place_arrival": self.arrival_place.value,  # место прибытия
                               "place_arrival2": self.arrival_place2.value,  # запасной (неактивный/активный)
                               "time_on": self.time_on.value,  # время включения двигателей (ДЛЯ РАСЧЕТА)
                               "time_off": self.time_off.value,  # время выключения двигателей (ДЛЯ РАСЧЕТА)
                               "time_departure": self.time_dep.value,  # время отрыва колес
                               "time_arrival": self.time_arr.value,  # время приземления
                               "time_PVP": self.time_PVP.value,  # время (неактивный/активный)
                               "time_PPP": self.time_PPP.value,  # время (неактивный/активный)
                               "ETD": self.etd.value,  # во сколько должны были взлететь
                               "ETA": self.eta.value,  # во сколько должны были сесть
                               "time_all": time_all,  # общее время от вкл до выкл (ДЛЯ РАСЧЕТА)
                               "time_air": t_air,  # общее время в воздухе
                               "time_day": time_day,  # от общего времени
                               "time_night": time_night,  # от общего времени
                               "time_PVP_PPP_all": '',  # ничего нет
                               "ETD_ETA_all": etd_eta}  # суммирование etd + eta
                print('set')
                try:
                    self.data.loc[self.data[(self.data['profile'] == self.profile) & (self.data['number'] == num) & (
                            self.data['date'] == self.date)].index[0]] = data_filled
                    print('rewrote')
                except:
                    self.data = self.data._append(data_filled, ignore_index=True)

                    print('added')



                print('calculated')

                self.profiles.to_csv("assets/profiles.csv", sep=',', index=False)
                self.data.to_csv("assets/data.csv", sep=',', index=False)
                print('saved')
                self.visual()
                self.pageadd.update()
                self.fill_menu.open = False
                self.fill_menu.update()

                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Введенные данные сохранены"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
                self.bs.open = True
                self.page.update()


            except:
                error = True
                error_handler('format')
                print("format error")

    # при изменении даты
    def change_date(self, e):

        self.date = " ".join(map(str, [self.date_picker.value.day, self.date_picker.value.month, self.date_picker.value.year]))
        self.date_vis = self.date_vision(self.date)
        self.pageadd.controls[0].controls[0].content.value = self.date_vis

        self.visual()
        self.pageadd.update()
        self.page.update()

