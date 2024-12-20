import webview
from tkinter import Tk, filedialog


def get_file_path(title: str  = "Выберите файл", filetypes: tuple = (("Все файлы", "*.*"),)):
    root = Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes
    )
    root.destroy()
    return file_path



class Window:

    def __init__(self, url: str, title: str = "pywebui window",
                size: tuple = (800, 600), min_size: tuple = (200, 100),
                resizable: bool = True, frameless: bool = False, easy_drag: bool = True,
                fullscreen: bool = False, icon: str = None, focus: bool = True, x: int = None, y: int = None,
                on_top: bool = False, background_color: str ="#FFFFFF", text_select: bool = False, transparent: bool = False):
        self.window = webview.create_window(
            title=title, url=url, min_size=min_size, width=size[0], height=size[1],
            resizable=resizable, focus=focus, fullscreen=fullscreen, frameless=frameless, easy_drag=easy_drag, x=x, y=y,
            on_top=on_top, background_color=background_color, text_select=text_select, transparent=transparent
        )

    def show(self):
        webview.start()
    
    def destroy(self):
        self.window.destroy()
    
    def move(self, x: int, y: int):
        self.window.move(x, y)
