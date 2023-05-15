import os

from django.conf import settings

def get_spider_dir():
    return settings.SPIDER_DIR

def create_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def write_code_to_py(filename, code):
    with open(filename, 'w') as f:
        f.write(code)

def save_spider_code(spidername, code):
    spider_dir = get_spider_dir()
    create_dir(spider_dir)
    spider_path = os.path.join(spider_dir, spidername+'.py')
    write_code_to_py(spider_path, code)
    return spider_path


class FakeOrderedList(list):

    def __init__(self,*args,**kwargs):
      self.ordered = True
      super().__init__(*args,**kwargs)

    def __repr__(self):
      return list.__repr__(self)
