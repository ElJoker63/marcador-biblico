import flet as ft

# -------------------
# Configuración de la aplicación
# -------------------
appbar_color = ft.Colors.WHITE

# Datos bíblicos simplificados
canon = {
    "Antiguo Testamento": [
        ("Gn", "Génesis", 50),
        ("Ex", "Éxodo", 40),
        ("Lv", "Levítico", 27),
        ("Nm", "Números", 36),
        ("Dt", "Deuteronomio", 34),
        ("Jos", "Josué", 24),
        ("Jue", "Jueces", 21),
        ("Rt", "Rut", 4),
        ("1 Sam", "1 Samuel", 31),
        ("2 Sam", "2 Samuel", 24),
        ("1 Re", "1 Reyes", 22),
        ("2 Re", "2 Reyes", 25),
        ("1 Cr", "1 Crónicas", 29),
        ("2 Cr", "2 Crónicas", 36),
        ("Esd", "Esdras", 10),
        ("Neh", "Nehemías", 13),
        ("Est", "Ester", 10),
        ("Job", "Job", 42),
        ("Sal", "Salmos", 150),
        ("Pr", "Proverbios", 31),
        ("Ecl", "Eclesiastés", 12),
        ("Cnt", "Cantares", 8),
        ("Is", "Isaías", 66),
        ("Jer", "Jeremías", 52),
        ("Lam", "Lamentaciones", 5),
        ("Ez", "Ezequiel", 48),
        ("Dn", "Daniel", 12),
        ("Os", "Oseas", 14),
        ("Jl", "Joel", 3),
        ("Am", "Amós", 9),
        ("Abd", "Abdías", 1),
        ("Jon", "Jonás", 4),
        ("Mi", "Miqueas", 7),
        ("Nah", "Nahúm", 3),
        ("Hab", "Habacuc", 3),
        ("Sof", "Sofonías", 3),
        ("Hag", "Hageo", 2),
        ("Zac", "Zacarías", 14),
        ("Mal", "Malaquías", 4)
    ],
    "Nuevo Testamento": [
        ("Mt", "Mateo", 28),
        ("Mr", "Marcos", 16),
        ("Lc", "Lucas", 24),
        ("Jn", "Juan", 21),
        ("Hch", "Hechos", 28),
        ("Ro", "Romanos", 16),
        ("1 Co", "1 Corintios", 16),
        ("2 Co", "2 Corintios", 13),
        ("Gl", "Gálatas", 6),
        ("Ef", "Efesios", 6),
        ("Flp", "Filipenses", 4),
        ("Col", "Colosenses", 4),
        ("1 Ts", "1 Tesalonicenses", 5),
        ("2 Ts", "2 Tesalonicenses", 3),
        ("1 Ti", "1 Timoteo", 6),
        ("2 Ti", "2 Timoteo", 4),
        ("Tit", "Tito", 3),
        ("Flm", "Filemón", 1),
        ("Heb", "Hebreos", 13),
        ("Stg", "Santiago", 5),
        ("1 Pe", "1 Pedro", 5),
        ("2 Pe", "2 Pedro", 3),
        ("1 Jn", "1 Juan", 5),
        ("2 Jn", "2 Juan", 1),
        ("3 Jn", "3 Juan", 1),
        ("Jud", "Judas", 1),
        ("Ap", "Apocalipsis", 22)
    ]
}

# -------------------
# Pantalla de capítulos
# -------------------
def mostrar_capitulos(pagina: ft.Page, abreviatura, nombre, total):
    lectura = pagina.client_storage.get("lectura") or {}
    print(lectura)  # Para depuración

    def toggle(e):
        cap = int(e.control.text)
        key = f"{abreviatura}_{cap}"
        lectura[key] = not lectura.get(key, False)
        pagina.client_storage.set("lectura", lectura)
        e.control.bgcolor = ft.Colors.GREEN if lectura[key] else ft.Colors.GREY_200
        pagina.update()

    botones = [
        ft.ElevatedButton(
            str(i+1),
            on_click=toggle,
            bgcolor=ft.Colors.GREEN if lectura.get(f"{abreviatura}_{i+1}", False) else ft.Colors.GREY_200,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ) for i in range(total)
    ]

    pagina.views.append(
        ft.View(
            route=f"/{abreviatura}",
            appbar=ft.AppBar(title=ft.Text(nombre), center_title=True, bgcolor=appbar_color),
            controls=[
                ft.Row(controls=botones, wrap=True, spacing=5, run_spacing=5),
            ]
        )
    )
    pagina.go(f"/{abreviatura}")

# -------------------
# Pantalla de libros
# -------------------
def mostrar_libros(pagina: ft.Page, testamento):
    lectura = pagina.client_storage.get("lectura") or {}
    libros = canon[testamento]
    botones = []
    for abrev, nombre, caps in libros:
        completado = all(lectura.get(f"{abrev}_{i+1}", False) for i in range(caps))
        botones.append(
            ft.ElevatedButton(
                abrev,
                bgcolor=ft.Colors.GREEN if completado else ft.Colors.GREY_200,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda e, a=abrev, n=nombre, t=caps: mostrar_capitulos(pagina, a, n, t)
            )
        )

    pagina.views.append(
        ft.View(
            route=f"/{testamento}",
            appbar=ft.AppBar(title=ft.Text(testamento), center_title=True, bgcolor=appbar_color),
            controls=[
                ft.Row(controls=botones, wrap=True, spacing=5, run_spacing=5),
            ]
        )
    )
    pagina.go(f"/{testamento}")

# -------------------
# Pantalla principal
# -------------------
def main(pagina: ft.Page):
    pagina.title = "Marcador Bíblico"
    pagina.theme_mode = ft.ThemeMode.LIGHT
    lectura = pagina.client_storage.get("lectura") or {}

    def iniciar(e):
        completo_at = all(
            all(lectura.get(f"{a}_{i+1}", False) for i in range(c))
            for a, _, c in canon["Antiguo Testamento"]
        )
        completo_nt = all(
            all(lectura.get(f"{a}_{i+1}", False) for i in range(c))
            for a, _, c in canon["Nuevo Testamento"]
        )
        at_color = ft.Colors.GREEN if completo_at else ft.Colors.BLUE_100
        nt_color = ft.Colors.GREEN if completo_nt else ft.Colors.BLUE_100

        pagina.views.clear()
        pagina.views.append(
            ft.View(
                route="/",
                appbar=ft.AppBar(leading=ft.Image(src='assets/icon.png'), title=ft.Text("Marcador Bíblico"), center_title=True,
                                bgcolor=appbar_color),
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Antiguo Testamento",
                                on_click=lambda _: mostrar_libros(pagina, "Antiguo Testamento"),
                                bgcolor=at_color,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                            ),
                            ft.ElevatedButton(
                                "Nuevo Testamento",
                                on_click=lambda _: mostrar_libros(pagina, "Nuevo Testamento"),
                                bgcolor=nt_color,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                            ),
                            ft.ElevatedButton(
                                "Configuración",
                                on_click=lambda _: mostrar_libros(pagina, "Configuración"),
                                bgcolor=ft.Colors.BLUE_100,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                            )
                        ],
                        expand=True,  # ocupa todo el alto disponible → permite centrar verticalmente
                        alignment=ft.MainAxisAlignment.CENTER,  # centra los controles **verticalmente**
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # centra **horizontalmente**
                        #spacing=24,
                    )
                ],
            ),
        )
        pagina.go("/")

    def retroceder(e):
        if len(pagina.views) > 1:
            pagina.views.pop()
            pagina.go(pagina.views[-1].route)

    pagina.on_view_pop = retroceder
    iniciar(None)

ft.app(target=main, assets_dir="assets")
