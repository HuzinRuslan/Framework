# import abc
#
#
# class SiteDB:
#     courses = ['Math', 'Physics', 'English']
#     categories = ['Web', 'GameDev', 'Ai']
#
#     def get_course(self, name):
#         for cat in self.courses:
#             if name == cat:
#                 return True
#             else:
#                 return False
#
#     def find_category_by_id(self, id):
#         category = self.categories[id]
#         return category
#
#     def create_course(self, name, category):
#         self.courses.append(name)
#
#
# class Course:
#     @abc.abstractmethod
#     def course_count(self):
#         pass
#
#
# class Math(Course):
#     def course_count(self):
#         pass
