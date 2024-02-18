import datetime as dt
import os
import pandas as pd
import flet as ft
import menu.profile
import menu.main_menu
import menu.settings
import menu.fly
import flyapp


class Main:

    if not os.path.exists("profiles.csv"):
        df = pd.DataFrame(
            columns=["profile_name", "fio", "company", "flytime_all", "flytime_day", "flytime_night", "add_all",
                     "add_day", "add_night"]).to_csv(
            'profiles.csv', index=False)

    if not os.path.exists("data.csv"):
        df2 = pd.DataFrame(
            columns=["profile", "date", "number", "plane_number", "flight", "place_departure", "place_arrival",
                     "place_arrival2",
                     "time_on", "time_off", "time_departure", "time_arrival", "time_PVP", "time_PPP", "ETD", "ETA",
                     "time_all", "time_air", "time_day", "time_night", "time_PVP_PPP_all", "ETD_ETA_all"]).to_csv(
            'data.csv', index=False)

    if not os.path.exists("data/current.txt"):
        with open("data/current.txt", "w") as file:
            file.write("<Не выбрано>")

    if not os.path.exists("data/airport.txt"):
        with open("data/airport.txt", "w") as file:
            file.write("IATA")

def main(page: ft.Page):
    main = Main()
    app = flyapp.FlyApp()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(outline="white"))





    page.title = ''
    page.bgcolor = '#2a2253'


    page.window_width = 400
    page.window_height = 800
    page.scroll = True
    page.tracemalloc = True


    deny = ft.BottomSheet(open=False)
    page.overlay.append(deny)


    prof = menu.profile.Start()
    mainm = menu.main_menu.Main_Menu()
    sett = menu.settings.Settings()
    flym = menu.fly.Fly_Menu()

    menu_nav = ()


    def deny_close(e):  # всплывающее окно запрета входа
        deny.open = False
        page.update()

    def open_main(e):  # проверка на выбор профиля и вход в главное меню
        if open('data/current.txt').readline() == '<Не выбрано>':
            deny.content = ft.Container(ft.Column([
                ft.Text("Вы не создали ни одного профиля!"),
                ft.ElevatedButton("Закрыть", on_click=deny_close)],
                tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            deny.open = True
            page.update()
        else:
            page.go("/main")

    fly_add = ft.Container(  # кнопка входа в меню полетов
        ft.Column(
            [
                ft.Text("Еще вылеты", width=90, color=app.dark_color, weight=ft.FontWeight.W_700, size=12,
                        text_align=ft.TextAlign.CENTER),
                ft.Image(
                    src='https://cdn-icons-png.flaticon.com/512/6329/6329169.png',
                    width=40,
                    height=40,
                    offset=ft.Offset(0, -0.2)
                )
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            offset=ft.Offset(0.0, 0.1)
        ),
        width=100,
        height=80,
        bgcolor=app.light_color,
        border_radius=20,
        on_click=lambda _: page.go('/fly'),
        shadow=ft.BoxShadow(
            blur_radius=5,
            color=app.extra_color,
            spread_radius=0.01,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )
    )

    prof_ch = ft.Container(  # кнопка входа в меню профилей из главного меню
        ft.Column(
            [
                ft.Text("Смена профиля", width=90, color=app.dark_color, weight=ft.FontWeight.W_700, size=11,
                        text_align=ft.TextAlign.CENTER),
                ft.Image(
                    src='https://cdn-icons-png.flaticon.com/512/8188/8188360.png',
                    width=40,
                    height=40,
                    offset=ft.Offset(0, -0.2)
                )
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            offset=ft.Offset(0.0, 0.1)
        ),
        width=100,
        height=80,
        bgcolor=app.light_color,
        border_radius=20,
        on_click=lambda _: page.go('profile'),
        shadow=ft.BoxShadow(
            blur_radius=5,
            color=app.extra_color,
            spread_radius=0.01,
            blur_style=ft.ShadowBlurStyle.OUTER,
        )

    )

    setting = ft.Container(  # кнопка настроек (ДОБАВЛЯЕТСЯ ЧЕРЕЗ APPEND)
                        ft.Image(
                            src='https://i.imgur.com/G2XTeE2.png',
                            width=40,
                            height=40,
                        ),
                        bgcolor=app.white,
                        width=55,
                        height=55,
                        border_radius=30,
                        alignment=ft.alignment.center,
                        offset=ft.Offset(-0.1,0.1),
                        right=1,
                        on_click=lambda e: return_to(page.route)
                    )

    setting_out = ft.Container(  # кнопка выхода из настроек (ДОБАВЛЯЕТСЯ ЧЕРЕЗ APPEND)
                        ft.Image(
                            src='https://cdn-icons-png.flaticon.com/512/507/507257.png',
                            width=30,
                            height=30,
                        ),
                        bgcolor=app.white,
                        width=55,
                        height=55,
                        border_radius=30,
                        alignment=ft.alignment.center,
                        offset=ft.Offset(0.1,0.1),
                        left=1,
                        on_click=lambda e: page.go(d)
                    )

    fly_out = ft.Container(  # кнопка выхода из меню полетов (ДОБАВЛЯЕТСЯ ЧЕРЕЗ APPEND)
        ft.Image(
            src='https://cdn-icons-png.flaticon.com/512/507/507257.png',
            width=30,
            height=30,
        ),
        bgcolor=app.white,
        width=55,
        height=55,
        border_radius=30,
        alignment=ft.alignment.center,
        offset=ft.Offset(0.1, 0.1),
        left=1,
        on_click=lambda e: page.go('/main')
    )

    def return_to(dest):  # механизм возврата к страницам, из которых вошли в настройки
        global d
        d = dest
        page.go('/settings')

    def route_change(route):  # выбор между страницами (сначала меню входа)
        page.views.clear()
        prof = menu.profile.Start()
        page.overlay.append(prof.bs); page.overlay.append(prof.ds); page.overlay.append(prof.es);



        page.views.append(
                ft.View(
                    "/",
                    [
                        prof.bar,
                        prof,
                        ft.ElevatedButton(
                            content=ft.Text(value="Войти", color='white', size=20),
                            bgcolor='#6bb4d6',
                            elevation=6,
                            width=400 - 200,
                            height=50,
                            offset=ft.Offset(0, -1.6),
                            on_click=open_main
                        )
                    ],
                    bgcolor=page.bgcolor,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=True
                )
        )
        if page.route == "/main":  # главное меню
            page.views.clear()
            mainm = menu.main_menu.Main_Menu()
            mainm.menubar.title.controls.append(setting)

            mainm.pageadd.controls[1].content.controls[3].controls[1] = fly_add
            mainm.pageadd.controls[1].content.controls[9].controls[1] = prof_ch

            page.overlay.append(mainm.date_picker)

            page.views.append(
                ft.View(
                    "/main",
                    [
                        mainm.menubar,
                        mainm,


                    ],
                    bgcolor=page.bgcolor,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=True

                )
            )
        if page.route == "/settings":  # настройки
            page.views.clear()
            sett = menu.settings.Settings()
            sett.menubar.title.controls.append(setting_out)
            page.overlay.append(sett.choose)
            page.overlay.append(sett.bs)
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        sett.menubar,
                        sett,
                    ],
                    bgcolor=page.bgcolor,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=True
                )
            )
        if page.route == "/fly":  # заполнение рейсов
            page.views.clear()

            mainm = menu.main_menu.Main_Menu()
            mainm.menubar.title.controls.append(setting)


            mainm.menubar.title.controls.append(fly_out)
            flym = menu.fly.Fly_Menu()
            page.overlay.append(flym.date_picker)
            page.overlay.append(flym.fill_menu)
            page.overlay.append(flym.bs)

            page.views.append(
                ft.View(
                    "/fly",
                    [
                        mainm.menubar,
                        flym
                    ],
                    bgcolor=page.bgcolor,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=True
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()




ft.app(target=main)





