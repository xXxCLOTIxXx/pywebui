from flask import Flask
from werkzeug.exceptions import NotFound
from flask_socketio import SocketIO, send, emit
from threading import Thread

from .respounse import render_template_path, send_from_directory, p
from ..window import get_file_path

socketio_file = p.join(p.dirname(__file__), 'base', 'socket.js')
socketio_part = f'<script src="pywebui/js/socket.js"></script>'


class FlaskServer:

    def __init__(self, import_name: str, host='127.0.0.1', port=5000,
                 static_folder: str = "static", template_folder="templates"):
        self.host = host
        self.port = port
        self.app = Flask(import_name, static_folder=static_folder, template_folder=template_folder)
        self.socket = SocketIO(self.app)
        self.screens_path = None

        self.add_route('/screen/<path:endpoint>', self.__screen_handler)

        @self.app.errorhandler(Exception)
        def handle_all_errors(error):
            code = getattr(error, 'code', 500)
            message = str(error)

            template_path = p.join(p.dirname(__file__), 'base', 'error.html')
            return render_template_path(template_path, message=message, code=code), code



        @self.app.route('/static/<path:filename>')
        def serve_static_file(filename):
            return send_from_directory(static_folder, filename)
        
        @self.app.route('/pywebui/<path:filename>')
        def serve_pywebui_file(filename):
            return send_from_directory(p.join(p.dirname(__file__), 'base'), filename), 200


        @self.socket.on('pywebui_file_dialog_request')
        def handle_file_dialog_request(data):
            request_id = data.get('id')
            wtitle = data.get('title', 'select file')

            def resp():
                file_path = get_file_path(title=wtitle)
                self.socket.emit('pywebui_filepath_response', {
                    'id': request_id,
                    'filePath': file_path
                })

            thread = Thread(target=resp, daemon=True)
            thread.start()



    def add_route(self, route, view_func, methods=['GET']):
        self.app.add_url_rule(route, view_func=view_func, methods=methods)


    def __screen_handler(self, endpoint):
        if self.screens_path:
            path = p.join(self.screens_path, endpoint)
            if p.exists(path):
                return render_template_path(path), 200
            raise NotFound(path)
        raise NotFound()


    def set_screens_path(self, path):
        self.screens_path=path

    def __run(self, debug):
        self.app.run(
            host=self.host, port=self.port,
            debug=debug, use_reloader=False
        )

    def start(self, debug: bool | None = None):
        flask_thread = Thread(target=self.__run, args=(debug,), daemon=True)
        flask_thread.start()
