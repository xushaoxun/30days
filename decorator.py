# coding:utf-8
import datetime
'''
装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，
装饰器的返回值也是一个函数对象。它经常用于有切面需求的场景，
比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。
装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。
概括的讲，装饰器的作用就是为已经存在的函数或对象添加额外的功能。
'''
def debug(func):
    def wrapper(*args, **kwargs):
        print('[DEBUG] enter:{}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper

@debug
def say_hello(user=None):
    print('hello', user)

# @debug
# def say_goodbye():
#     print('goodbye')

say_hello('aa')
print('*'*20)

#闭包可以被理解为一个只读的对象，你可以给他传递一个属性，但它只能提供给你一个执行的接口。
def func(name):
    def inner_func(age):
        print('{} is {}'.format(name, age))
    return inner_func

f = func('eagle')# 调用func的时候就产生了一个闭包——inner_func,并且该闭包持有自由变量——name
f(25)

print('*'*20)

def partial(**outer_kwargs):
    def wrapper(func):
        def inner(*args, **kwargs):
            for k,v in outer_kwargs.items():
                kwargs[k] = v
            return func(*args, **kwargs)
        return inner
    return wrapper

@partial(name='eagle')
def say(name=None, age=None):
    print('{} is {}'.format(name, age))

say(age=11)

print('*'*20)
def tag(tag_name):
    def add_tag(content):
        return '<{0}>{1}</{0}>'.format(tag_name, content)
    return add_tag

add_tag = tag('a')

#闭包函数相对与普通函数会多出一个__closure__的属性，
# 里面定义了一个元组用于存放所有的cell对象，每个cell对象一一保存了这个闭包中所有的外部变量
print(add_tag.__closure__)
print(add_tag('link'))

print('*'*20)

def log(level):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            print('[{}] {}'.format(level, func.__name__))
            return func(*args, **kwargs)
        return inner_wrapper
    return wrapper

@log('INFO')
def f():
    print('do something in f')

f()

print('*'*20)
class debug():
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('debug: ', self.func.__name__)
        return self.func(*args, **kwargs)

@debug
def ff(name):
    print('i am', name)
ff('eagle')

print('*'*20)
class logging():
    def __init__(self, level):
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):

            print('{}: {}'.format(self.level, func.__name__))
            return func(*args, **kwargs)
        return wrapper

@logging('WARN')
def fff(name, age):
    print('{} is {}'.format(name, age))
fff('eagle', 25)

print('*'*20)
class Animal():
    def __init__(self, birth_year):
        self.birth_year = birth_year

    @property
    def age(self):
        return datetime.date.today().year - self.birth_year


    @staticmethod
    def bark():
        print('bark')

    @classmethod
    def eat(cls):
        instance = cls(1981)
        print(instance)


a = Animal(2000)
print(a.age)
Animal.bark()
Animal.eat()