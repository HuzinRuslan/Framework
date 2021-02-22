from MyFramework.core import Application
import views

urls = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/authors/': views.Authors(),
    '/contact/': views.contact_view,
    '/create-course/': views.create_course,
    '/create-category/': views.create_category,
    '/course-list/': views.course_list,
    '/category-list/': views.category_list,
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urls, front_controllers)

