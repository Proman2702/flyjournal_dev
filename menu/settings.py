import flet as ft
import pandas as pd
import datetime
import flyapp
import calc.time_parser

class Settings(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.appbar_height = 115
        self.app = flyapp.FlyApp()
        self.code = open('data/airport.txt').readline()
        self.profile = open('data/current.txt').readline()
        self.data = pd.read_csv('data.csv')
        self.date = " ".join(map(str, [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]))
        self.bs = ft.BottomSheet(open=False)  # всплывающие окна
        self.choose = ft.AlertDialog(
            actions=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text('День', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'd')
                                ),
                                ft.Container(
                                    content=ft.Text('Неделя', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'w')
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text('Месяц', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'm')
                                ),
                                ft.Container(
                                    content=ft.Text('Квартал', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'q')
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text('Год', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'y')
                                ),
                                ft.Container(
                                    content=ft.Text('Все время', color=self.app.extra_color, size=16, weight=ft.FontWeight.W_700),
                                    border_radius=20,
                                    bgcolor=self.app.white,
                                    width=120,
                                    height=80,
                                    shadow=ft.BoxShadow(
                                        blur_radius=2,
                                        color=self.app.extra_color,
                                        spread_radius=1,
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    on_click=lambda _: self.make_export(_, 'x')
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, offset=ft.Offset(0.0,0.02)
                )
            ],
            title=ft.Text('Выберите формат экспорта', color=self.app.extra_color, size=18, weight=ft.FontWeight.W_700),
            inset_padding=ft.padding.symmetric(vertical=60, horizontal=5),
            title_padding=ft.padding.symmetric(vertical=10, horizontal=20)
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
                                ft.Text(f"Настройки", color=self.app.dark_color, font_family='Consolas', size=25,
                                        weight=ft.FontWeight.W_700)
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
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                ft.Text('Сменить профиль', color=self.app.dark_color, size=19, weight=ft.FontWeight.W_600),
                                height=60,
                                width=310,
                                border_radius=30,
                                alignment=ft.alignment.center,
                                bgcolor=self.app.light_color,
                                shadow=ft.BoxShadow(
                                    blur_radius=5,
                                    color=self.app.extra_color,
                                    spread_radius=0.01,
                                    blur_style=ft.ShadowBlurStyle.OUTER,
                                ),
                                on_click=lambda e: self.page.go('/')
                            ),
                            ft.Container(
                                ft.Text(f'Код аэропортов: <{self.code}>', color=self.app.dark_color, size=19,
                                        weight=ft.FontWeight.W_600),
                                height=60,
                                width=310,
                                border_radius=30,
                                alignment=ft.alignment.center,
                                bgcolor=self.app.light_color,
                                shadow=ft.BoxShadow(
                                    blur_radius=5,
                                    color=self.app.extra_color,
                                    spread_radius=0.01,
                                    blur_style=ft.ShadowBlurStyle.OUTER,
                                ),
                                on_click=self.change_code
                            ),
                            ft.Container(
                                ft.Text('Экспорт в EXCEL', color=self.app.dark_color, size=19,
                                        weight=ft.FontWeight.W_600),
                                height=60,
                                width=310,
                                border_radius=30,
                                alignment=ft.alignment.center,
                                bgcolor=self.app.light_color,
                                shadow=ft.BoxShadow(
                                    blur_radius=5,
                                    color=self.app.extra_color,
                                    spread_radius=0.01,
                                    blur_style=ft.ShadowBlurStyle.OUTER,
                                ),
                                on_click=self.open_export
                            ),
                        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, offset=(0.0,0.03)
                    ),
                    bgcolor=self.app.white,
                    width=400 - 50,
                    height=600,
                    border_radius=30
                )
            ],
            spacing=100,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )


    def open_export(self, e):
        self.choose.open = True
        self.choose.update()

    def pd_time(self):
        return 1

    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    def make_export(self, e, period):

        csv = calc.time_parser.Calc(date=self.date, csv=self.data, period=period, profile=self.profile).parser()
        csv['date'] = csv['date'].dt.strftime('%Y-%m-%d')
        csv.to_excel('fly_data.xlsx', index=False)
        self.bs.content = ft.Container(ft.Column([
            ft.Text("Данные были экспортированы в загрузки"),
            ft.ElevatedButton("Закрыть", on_click=self.close_bs),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        self.bs.open = True
        self.choose.open = False
        self.choose.update()
        self.bs.update()

    # изменение IATA/ICAO
    def change_code(self, e):
        if self.code == 'IATA':
            self.code = 'ICAO'
            self.pageadd.controls[0].content.controls[1].content = ft.Text(f'Код аэропортов: <{self.code}>', color=self.app.dark_color, size=19,weight=ft.FontWeight.W_600)
            with open("data/airport.txt", "w") as file:
                file.write(self.code)
            self.pageadd.update()
            self.page.update()
        elif self.code == 'ICAO':
            self.code = 'IATA'
            self.pageadd.controls[0].content.controls[1].content = ft.Text(f'Код аэропортов: <{self.code}>',
                                                                                 color=self.app.dark_color, size=19,
                                                                                 weight=ft.FontWeight.W_600)
            with open("data/airport.txt", "w") as file:
                file.write(self.code)
            self.pageadd.update()
            self.page.update()
    def build(self):
        return self.pageadd
