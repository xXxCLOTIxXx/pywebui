from .window import Window
from .server.flask import FlaskServer


class App(Window, FlaskServer):
    def __init__(self, import_name: str, host: str = '127.0.0.1', port: int = 5000, static_folder: str = "static", template_folder="templates", title: str = "pywebui window", size: tuple = (800, 600), min_size: tuple = (200, 100), resizable: bool = True, frameless: bool = False, easy_drag: bool = True, fullscreen: bool = False, focus: bool = True, x: int = None, y: int = None, on_top: bool = False, background_color: str = "#FFFFFF", text_select: bool = False, transparent: bool = False, initial_page: str = None):
        self.flask = FlaskServer(import_name, host, port, static_folder, template_folder)
        self.window = Window(
            f"http://{self.flask.host}:{self.flask.port}",
            title, size, min_size, resizable, frameless, easy_drag,
            fullscreen, focus, x, y, on_top, background_color,
            text_select, transparent, initial_page

        )

    def run(self, debug: bool | None = None):
        self.flask.start(debug)
        self.window.show()