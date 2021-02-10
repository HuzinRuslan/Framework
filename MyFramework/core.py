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

        if path in self.urls:
            # получаем view по url
            view = self.urls[path]
            request = {}
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
