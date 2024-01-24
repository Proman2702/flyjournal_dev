import flet as ft

def main(page: ft.Page):
    page.title = "Containers - clickable and not"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = '#2a2253'
    page.window_width = 400
    page.window_height = 800
    page.scroll = True
    h_toolbar = 115

    page.appbar = ft.AppBar(
        bgcolor='#2a2253',
        leading_width=0,
        toolbar_height=h_toolbar,
        center_title=True,
        title=ft.Stack([


            ft.Container(
                content=ft.Column(controls=[
                    ft.Text("Виталий", color=page.bgcolor, weight=ft.FontWeight.W_900),
                    ft.Text("Boeing777", color=page.bgcolor)
                ],spacing=0, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                width=page.window_width-50,
                height=h_toolbar-50,
                border_radius=ft.border_radius.all(30),
                bgcolor='#d8eef8'
            ),
            ft.Container(
                content=ft.Image(
                    src=f'https://cdn.onlinewebfonts.com/svg/img_120429.png',
                    fit=ft.ImageFit.FILL,
                    height=40,
                    width=40
                ),
                bgcolor='#ffffff',
                width=h_toolbar - 60,
                height=h_toolbar - 60,
                alignment=ft.alignment.center,
                right=7,
                bottom=5,
                border_radius=ft.border_radius.all((h_toolbar - 60)//2)
            )
        ]),
        actions=[]
    )




    page.add(ft.Column([ft.Container(),

        ft.Stack(
                [
                    ft.Container(
                        content=ft.Text(""),
                        alignment=ft.alignment.center,
                        bgcolor='#ffffff',
                        width=page.window_width - 50,
                        padding=-100,
                        height=1000,
                        border_radius=30,
                    )
                ]
            )
        ], spacing=100, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    )

ft.app(target=main)