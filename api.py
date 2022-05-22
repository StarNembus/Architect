
from webob import Request, Response
from parse import parse


class Main:
    #  В методе __init__ определяю словарь под названием self.routes,
    #  в котором будут пути в качестве ключей, а обработчики - в качестве значений
    def __init__(self):
        self.routes = {}

    # route является декоратором, принимает путь и оборачивает методы
    def route(self, path):
        """
        В методе route, берем путь в качестве аргумента
        :param path:
        :return:
        """
        def wrapper(handler):
            """
            вносим путь в словарь self.routes
            :param handler:
            :return:
            """
            self.routes[path] = handler
            print(self.routes)
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    # обработчик пути
    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def default_response(self, response):
        """
        метод, который возвращает простой HTTP ответ “не найдено” со статусом кода 404
        :param response:
        :return:
        """
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
