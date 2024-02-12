import pandas as pd
import flet as ft
import datetime
import flyapp

class Fly_Menu(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.app = flyapp.FlyApp()
        self.profile = open('data/current.txt').readline()
        self.date = " ".join(map(str, [datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year]))
        self.date_vis = self.date_vision(self.date)

        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            first_date=datetime.datetime(2000, 10, 1),
            last_date=datetime.datetime.now(),
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
                            offset=ft.Offset(0.0, 0.0)
                        ),
                        ft.Container(
                            ft.Image(
                                src='https://i.imgur.com/dNiaTTh.png',
                                width=40,
                                height=40,
                                offset=ft.Offset(0.0, 0.0)
                            ),
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            bgcolor=self.app.white,
                            border_radius=30,
                            offset=ft.Offset(-0.3, 0.0),
                            on_click=lambda _: self.date_picker.pick_date(),
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0, offset=ft.Offset(0.05, 0.5)
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
                            ft.Container(
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center
                            ),
                            ft.Row(
                                [
                                    ft.Text("2 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center
                            ),
                            ft.Row(
                                [
                                    ft.Text("3 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center
                            ),
                            ft.Row(
                                [
                                    ft.Text("4 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center
                            ),
                            ft.Row(
                                [
                                    ft.Text("5 полет:", size=16, color=self.app.light_color, width=70, height=30,
                                            weight=ft.FontWeight.W_600),
                                    ft.Container(bgcolor=self.app.light_color, width=220, height=2, border_radius=10)
                                ], spacing=10, alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, offset=(0.05, 0.0)
                            ),
                            ft.Container(
                                content=ft.Row(),
                                bgcolor=self.app.light_color,
                                width=320,
                                height=80,
                                border_radius=20,
                                alignment=ft.alignment.center
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

    def date_vision(self, t):
        d = t.split(" ")[0]
        m = t.split(" ")[1]
        y = t.split(" ")[2]

        if len(d) == 1:
            d = "0" + d
        if len(m) == 1:
            m = "0" + m

        return f"{d}.{m}.{y}"

    def change_date(self, e):


        self.date = " ".join(map(str, [self.date_picker.value.day, self.date_picker.value.month, self.date_picker.value.year]))
        self.date_vis = self.date_vision(self.date)
        self.pageadd.controls[0].controls[0].content.value = self.date_vis

        self.pageadd.update()
        self.page.update()
    def build(self):
        return self.pageadd
