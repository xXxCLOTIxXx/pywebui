from pywebui import App
app = App(__name__, initial_page = '/screen/home.html')
app.flask.set_screens_path("screens")

if __name__ == "__main__":
    app.run()