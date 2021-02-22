from reusepatterns.singletones import SingletonByName
import time


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text, time.asctime())
