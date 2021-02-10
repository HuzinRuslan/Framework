from templator import render


# page controller
class Main:

    def __call__(self, request):
        html = render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])

        return '200 OK', [html.encode('utf-8')]


class Other:

    def __call__(self, request):
        print(request)
        return '200 OK', [b'<h1>other</h1>']


def catalog(request):
    print(request)
    return '200 OK', [b'catalog']


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 PAGE Not Found']


urls = {
    '/': Main(),
    '/catalog/': catalog,
    '/other/': Other()
}


# Front controllers
def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


class Application:

    def __init__(self, urls, fronts):
        self.urls = urls
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.urls:
            view = self.urls[path]
        else:
            view = not_found_404_view
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(urls, fronts)
