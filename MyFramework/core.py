import quopri


class Application:

    def __init__(self, urls: dict, front_controllers: list):
        """
        :param urls: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.urls = urls
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        # текущий url
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем все данные POST запроса
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        # Получаем все данные GET запроса
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urls:
            # получаем view по url
            view = self.urls[path]
            request = {}

            # добавляем параметры запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)

            # вызываем view, получаем результат
            code, body = view(request)

            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])

            # возвращаем тело ответа
            return [body.encode('utf-8')]
        else:
            # Если url нет в urlpatterns - то страница не найдена
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]

    def parse_wsgi_input_data(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    @staticmethod
    def get_wsgi_input_data(environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def parse_input_data(data):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')
