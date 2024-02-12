
import pandas as pd
import flet as ft
import flyapp


class Start(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.appbar_height = 115
        self.profile = open('data/current.txt').readline()  # название профиля
        self.app = flyapp.FlyApp()  # класс настроек
        self.deleting_prof = ''  # какой профиль удаляется
        self.vis_profile = ft.Text(f"{self.app.version}", color=self.app.dark_color,  # версия приложения
                                   weight=ft.FontWeight.W_800, font_family='Consolas', size=24)
        self.ds, self.bs, self.es = ft.BottomSheet(open=False), ft.BottomSheet(open=False), ft.BottomSheet(open=False)  # всплывающие окна
        self.prof_name = ft.Text(value=f'{self.profile}', color=self.app.dark_color,  # отображение имени профиля
                weight=ft.FontWeight.W_700,
                font_family='Consolas', size=18)


        # поля для ввода данных при создании профиля
        self.a = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False)
        self.b = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False)
        self.c = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=False)
        self.d = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='0')
        self.e1 = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='0')
        self.f = ft.TextField(width=130, height=40, border_radius=25, bgcolor=self.app.white, border_color=self.app.light_color,
                              content_padding=ft.Padding(10.0, 0.0, 10.0, 0.0), disabled=True, value='0')

        self.cr_menu = ft.AlertDialog(  # меню создания новых профилей
            title=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Тип самолета", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600,
                                        width=110, height=50, offset=ft.Offset(-0.1, 0.2)),
                                self.a
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Text("ФИО", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600, width=110,
                                        height=45, offset=ft.Offset(-0.1, 0.2)),
                                self.b
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Text("Авиакомпания", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600,
                                        width=110, height=50, offset=ft.Offset(-0.1, 0.2)),
                                self.c
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Text("Часы налета днем", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600,
                                        width=110, height=50, offset=ft.Offset(-0.1, 0.2)),
                                self.d
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Text("Часы налета ночью", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600,
                                        width=110, height=50, offset=ft.Offset(-0.1, 0.2)),
                                self.e1
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Text("Общие часы налета", color=self.app.dark_color, size=15, weight=ft.FontWeight.W_600,
                                        width=110, height=50, offset=ft.Offset(-0.1, 0.2)),
                                self.f
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Checkbox(label="Добавить доп. часы налета", scale=0.6, offset=ft.Offset(-0.1, 0.0),
                                    on_change=self.checkbox),
                        ft.ElevatedButton("Сохранить",
                                          on_click=self.profile_creation_end)

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            ),
        )
        self.ch_menu = ft.AlertDialog(  # меню выбора профиля
            title=ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text('Выберите профиль:', color=self.app.extra_color, size=17,
                                            weight=ft.FontWeight.W_800),
                            width=200,
                            height=30,
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        self.scroll_list
                    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        )
        self.del_menu = ft.AlertDialog(  # меню выбора удаления профиля
            title=ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Text('Выберите профиль:', color="red", size=17,
                                            weight=ft.FontWeight.W_800),
                            width=200,
                            height=30,
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        self.scroll_list
                    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        )

        self.bar = ft.AppBar(
            bgcolor=self.app.dark_color,
            toolbar_height=self.appbar_height,
            center_title=True,
            title=ft.Stack(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(f"{self.app.title}", color=self.app.dark_color, font_family='Consolas', size=25,
                                        weight=ft.FontWeight.W_600),
                                self.vis_profile
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        bgcolor=self.app.light_color,
                        width=350,
                        height=self.appbar_height - 50,
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(30)
                    ),
                    ft.Container(
                        ft.Image(
                            src='img/nik.png',
                            width=50,
                            height=50,
                        ),
                        bgcolor=self.app.extra_color,
                        width=60,
                        height=60,
                        border_radius=30,
                        offset=ft.Offset(0.05, 0.05),
                        alignment=ft.alignment.center
                    )
                ]
            ),
            actions=[]
        )

        self.pageadd = ft.Column(
            [
                ft.Container(
                    content=ft.Text("Добро", color=self.app.light_color, size=25, weight=ft.FontWeight.W_700),
                    bgcolor=self.app.test_color,
                    border_radius=ft.border_radius.all(30),
                    alignment=ft.alignment.center,
                    width=200,
                    height=50,
                    offset=ft.Offset(-0.3, 0.3)
                ),
                ft.Container(
                    content=ft.Text("пожаловать", color=self.app.light_color, size=25, weight=ft.FontWeight.W_700),
                    bgcolor=self.app.test_color,
                    border_radius=ft.border_radius.all(30),
                    alignment=ft.alignment.center,
                    width=240,
                    height=50,
                    offset=ft.Offset(0.15, -0.2)
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(f"Профиль:", color=self.app.extra_color, size=16,
                                                weight=ft.FontWeight.W_600),
                                        self.prof_name
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                alignment=ft.alignment.center,
                                bgcolor=self.app.light_color,
                                width=400 - 80,
                                height=50,
                                border_radius=30,
                                offset=ft.Offset(0, 0.4),

                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [

                                                ft.Text(value="Выбрать профиль из списка", color=self.app.dark_color,
                                                        size=13, width=120, height=40, text_align=ft.TextAlign.CENTER,
                                                        weight=ft.FontWeight.W_800),
                                                ft.Image(
                                                    src='https://cdn-icons-png.flaticon.com/512/6704/6704979.png',
                                                    width=45,
                                                    height=35,
                                                    offset=ft.Offset(0, -0.05)
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=0,
                                            offset=ft.Offset(0, 0.01)

                                        ),
                                        alignment=ft.alignment.center,
                                        bgcolor=self.app.light_color,
                                        width=150,
                                        height=100,
                                        border_radius=30,
                                        on_click=self.profile_list,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                        )
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [

                                                ft.Text(value="Загрузить прошлый профиль", color=self.app.dark_color,
                                                        size=13, width=120, height=40, text_align=ft.TextAlign.CENTER,
                                                        weight=ft.FontWeight.W_800),
                                                ft.Image(
                                                    src='https://cdn-icons-png.flaticon.com/512/11497/11497200.png',
                                                    width=45,
                                                    height=35,
                                                    offset=ft.Offset(0, -0.05)
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=0,
                                            offset=ft.Offset(0, 0.01)

                                        ),
                                        alignment=ft.alignment.center,
                                        bgcolor=self.app.light_color,
                                        width=150,
                                        height=100,
                                        border_radius=30,
                                        on_click=self.open_es,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                        )
                                    )
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                offset=ft.Offset(0, 0.2)
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [

                                                ft.Text(value="Удалить профиль", color=self.app.dark_color,
                                                        size=13, width=140, height=40, text_align=ft.TextAlign.CENTER,
                                                        weight=ft.FontWeight.W_800),
                                                ft.Image(
                                                    src='https://cdn-icons-png.flaticon.com/512/1276/1276444.png',
                                                    width=30,
                                                    height=30,
                                                    offset=ft.Offset(0, -0.3)
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=0,
                                            offset=ft.Offset(0, 0.01),

                                        ),
                                        alignment=ft.alignment.center,
                                        bgcolor=self.app.light_color,
                                        width=150,
                                        height=100,
                                        border_radius=30,
                                        on_click=self.profile_delete,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                        )
                                    ),
                                    ft.Container(  # Создание
                                        content=ft.Column(
                                            [

                                                ft.Text(value="Создать новый профиль", color=self.app.dark_color,
                                                        size=13, width=120, height=40, text_align=ft.TextAlign.CENTER,
                                                        weight=ft.FontWeight.W_800),
                                                ft.Image(
                                                    src='https://cdn-icons-png.flaticon.com/512/6329/6329169.png',
                                                    width=45,
                                                    height=35,
                                                    offset=ft.Offset(0, -0.05)
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=0,
                                            offset=ft.Offset(0, 0.01),
                                        ),
                                        alignment=ft.alignment.center,
                                        bgcolor=self.app.light_color,
                                        width=150,
                                        height=100,
                                        border_radius=30,
                                        on_click=self.profile_creation,
                                        shadow=ft.BoxShadow(
                                            blur_radius=5,
                                            color=self.app.extra_color,
                                            spread_radius=0.01,
                                            blur_style=ft.ShadowBlurStyle.OUTER
                                        )
                                    )
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                offset=ft.Offset(0, 0.2)
                            ),
                            ft.Container(
                                bgcolor=self.app.white,
                                width=400 - 200,
                                height=50,
                                offset=ft.Offset(0, 0.5)

                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,

                    ),
                    bgcolor=self.app.white,
                    width=400 - 50,
                    height=400,
                    border_radius=30
                )
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def profile_chosen(self, e):  # если профиль был выбран

        self.profile = e.control.content.value
        self.pageadd.controls[2].content.controls[0].content.controls[1].value = self.profile
        with open("data/current.txt", "w") as file:
            file.write(self.profile)
        self.ch_menu.open = False
        self.pageadd.update()
        self.page.update()

    def build(self):
        return self.pageadd

    def close_bs(self, e):  # закрытие окна ошибки создания профиля
        self.bs.open = False
        self.bs.update()

    def open_es(self, e):
        if open("data/current.txt").readline() == '<Не выбрано>':
            self.es.content = ft.Container(ft.Column([
                ft.Text("Вы не создали ни одного профиля!"),
                ft.ElevatedButton("Закрыть", on_click=self.close_es)],
                tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        else:
            self.es.content = ft.Container(ft.Column([
                ft.Text("Прошлый профиль уже выбран!"),
                ft.ElevatedButton("Закрыть", on_click=self.close_es)],
                tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        self.es.open = True
        self.es.update()

    def close_es(self, e):  # закрытие окна выбора прошлого профиля
        self.es.open = False
        self.es.update()

    def close_ds_normal(self, e):  # закрытие окна ошибки удаления профиля
        self.ds.open = False
        self.ds.update()

    def close_ds(self, e):  # закрытие окна предупреждения об удалении профиля
        profiles = pd.read_csv('profiles.csv', dtype=str)
        profiles = profiles.drop(profiles.index[profiles['profile_name'] == self.deleting_prof][0]).reset_index(drop=True)
        profiles.to_csv("profiles.csv", sep=',', index=False)
        self.ds.open = False
        self.del_menu.open = False
        self.page.update()

    def profile_creation(self, e):  # всплывание меню заполнения информации о профиле
        self.page.dialog = self.cr_menu
        self.cr_menu.open = True
        self.page.update()

    def profile_list(self, e):  # всплывание меню выбора профиля
        self.fill_scroll_list_chosen()
        self.page.dialog = self.ch_menu
        self.ch_menu.open = True
        self.page.update()

    def profile_delete(self, e): # всплывание меню выбора удаления профиля
        self.fill_scroll_list_delete()
        self.page.dialog = self.del_menu
        self.del_menu.open = True
        self.page.update()

    def checkbox(self, e):  # вкл/выкл ввод доп. часов налета
        if self.e1.disabled:
            self.e1.disabled = False; self.d.disabled = False; self.f.disabled = False
        else:
            self.e1.disabled = True; self.e1.value = '0'; self.d.disabled = True; self.d.value = '0'; self.f.disabled = True; self.f.value = '0'
        self.page.update()

    scroll_list = ft.ListView(spacing=20, height=300)




    def profile_delete_chosen(self, e): #если был выбран профиль на удаление
        self.deleting_prof = e.control.content.value
        if self.deleting_prof == self.profile:
            self.ds.content = ft.Container(ft.Column([
                ft.Text("Вы не можете удалить текущий профиль"),
                ft.ElevatedButton("Закрыть", on_click=self.close_ds_normal),
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        else:
            self.ds.content = ft.Container(ft.Column([
                ft.Text("Вы точно хотите удалить профиль?"),
                ft.ElevatedButton("Удалить", on_click=self.close_ds),
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        self.ds.open = True
        self.page.update()

    def fill_scroll_list_chosen(self):
        profiles = pd.read_csv('profiles.csv')
        self.scroll_list.controls = []
        for i in list(profiles['profile_name']):  # заполнение профилями список на выбор
            self.scroll_list.controls.append(ft.Row(
                [
                    ft.Container(
                        content=ft.Text(f'{i}', text_align=ft.TextAlign.CENTER, color=self.app.extra_color, size = 17, weight=ft.FontWeight.W_600),
                        width=200,
                        height=40,
                        bgcolor=self.app.white,
                        border_radius=30,
                        alignment=ft.alignment.center,
                        ink=True,
                        on_click=self.profile_chosen
                    )
                ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            ))


    def fill_scroll_list_delete(self):
        profiles = pd.read_csv('profiles.csv')
        self.scroll_list.controls = []
        for i in list(profiles['profile_name']):  # заполнение профилями список на удаление
            self.scroll_list.controls.append(ft.Row(
                [
                    ft.Container(
                        content=ft.Text(f'{i}', text_align=ft.TextAlign.CENTER, color="red", size = 17, weight=ft.FontWeight.W_600),
                        width=200,
                        height=40,
                        bgcolor=self.app.white,
                        border_radius=30,
                        alignment=ft.alignment.center,
                        ink=True,
                        on_click=self.profile_delete_chosen
                    )
                ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER
            ))

    def profile_creation_end(self, e):  # Проверка введенных данных

        profiles = pd.read_csv('profiles.csv')
        error = False

        def error_handler(t):
            if t == 'not_filled':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, поле не заполнено"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            if t == 'exists':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, такой профиль уже существует"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            if t == 'not_int':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, введенный текст не число"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            if t == 'comparing':
                self.bs.content = ft.Container(ft.Column([
                    ft.Text("Ошибка, общих часов больше, чем сумма дневных и ночных"),
                    ft.ElevatedButton("Закрыть", on_click=self.close_bs),
                ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
            self.bs.open = True
            self.page.update()

        if self.a.value == '': self.a.bgcolor = self.app.error_color; error = True; error_handler('not_filled')
        else: self.a.bgcolor = self.app.white

        if self.b.value == '': self.b.bgcolor = self.app.error_color; error = True; error_handler('not_filled')
        else: self.b.bgcolor = self.app.white

        if self.c.value == '': self.c.bgcolor = self.app.error_color; error = True; error_handler('not_filled')
        else: self.c.bgcolor = self.app.white

        if self.d.disabled: self.d.bgcolor = self.app.white; self.e1.bgcolor = self.app.white; self.f.bgcolor = self.app.white
        else:
            try: int(self.d.value); self.d.bgcolor = self.app.white
            except: self.d.bgcolor = self.app.error_color; error = True; self.d.value = ''; error_handler('not_int')

            try: int(self.e1.value); self.e1.bgcolor = self.app.white
            except: self.e1.bgcolor = self.app.error_color; error = True; self.e1.value = ''; error_handler('not_int');

            try: int(self.f.value); self.f.bgcolor = self.app.white
            except: self.f.bgcolor = self.app.error_color; error = True; self.f.value = ''; error_handler('not_int')


        if not error:
            if int(self.d.value) + int(self.e1.value) == int(self.f.value):
                profile_filled = {
                    'profile_name': self.a.value,
                    'fio': self.b.value,
                    'company': self.c.value,
                    'flytime_all': 0,
                    'flytime_day': 0,
                    'flytime_night': 0,
                    'add_all': int(self.f.value),
                    'add_day': int(self.d.value),
                    'add_night': int(self.e1.value)
                }

                if self.a.value in list(profiles['profile_name']):
                    self.a.bgcolor = self.app.error_color
                    self.a.value = ''
                    error_handler('exists')

                else:
                    profiles = profiles._append(profile_filled, ignore_index=True)
                    profile = self.a.value
                    profiles.to_csv("profiles.csv", sep=',', index=False)
                    self.page.dialog = self.cr_menu
                    self.cr_menu.open = False

            else:
                self.f.bgcolor = self.app.error_color
                self.f.value = ''
                error_handler('comparing')

        self.page.update()



























