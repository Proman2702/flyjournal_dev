import flet as ft
import flyapp

class Settings(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.appbar_height = 115
        self.app = flyapp.FlyApp()
        self.code = open('data/airport.txt').readline()
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
                                height=40,
                                width=300,
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
                                height=40,
                                width=300,
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
