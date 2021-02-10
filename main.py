from MyFramework.core import Application
import views

urls = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/authors/': views.Authors(),
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urls, front_controllers)

