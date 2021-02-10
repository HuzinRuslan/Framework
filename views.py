from MyFramework.templates import render


def main_view(request):
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    # Просто возвращаем текст
    return '200 OK', "About"


class Authors:

    def __call__(self, request):

        return '200 OK', render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
