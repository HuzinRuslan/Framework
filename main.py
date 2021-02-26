from MyFramework import render, Application, DebugApplication, FakeApplication
from models import TrainingSite
from logging_mod import Logger, debug

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log('Список курсов')
    print(f'Список курсов - {site.courses}')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def about_view(request):
    # Просто возвращаем текст
    return '200 OK', "About"


@debug
def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        data = request['data']
        title = Application.decode_value(data['title'])
        text = Application.decode_value(data['text'])
        email = Application.decode_value(data['email'])
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')


class Authors:

    def __call__(self, request):
        return '200 OK', render('authors.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])


urls = {
    '/': main_view,
    '/about/': about_view,
    '/authors/': Authors(),
    '/contact/': contact_view,
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urls, front_controllers)

# application = DebugApplication(urls, front_controllers)
# application = FakeApplication(urls, front_controllers)

@application.add_route('/create-course/')
def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')

        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


@application.add_route('/create-category/')
def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']

        name = Application.decode_value(name)

        new_category = site.create_category(name)

        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


@application.add_route('/course-list/')
def course_list(request):
    request_params = request['request_params']

    name = request_params['name']

    old_course = site.get_course(name)

    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)
