# coding:utf-8
from config import DB_URI, DATABASE_NAME, DB_HOST, DB_PORT
from mongoengine import connect, Document, DoesNotExist
from mongoengine.fields import StringField, IntField, DateTimeField, URLField, FileField, BooleanField
import datetime

def lazy_connect():
    connect(DATABASE_NAME, host=DB_HOST, port=DB_PORT)
lazy_connect()

class BaseModel(Document):
    create_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }

class Proxy(BaseModel):
    address = StringField(required=True, unique=True)
    from_site= StringField(required=True)

    @classmethod
    def get_random_proxy(cls):
        '''
        :return: str
        '''
        return cls.objects.aggregate({'$sample':{'size':1}}).next()['address']


    @classmethod
    def del_proxy(cls, address):
        try:
            Proxy.objects.get(address=address).delete()
        except DoesNotExist:
            pass

class Country(BaseModel):
    name = StringField(required=True, unique=True)
    url = URLField(required=True)
    flag_url = StringField(required=True)
    flag_path = StringField()

    area = IntField()
    population = IntField()
    iso = StringField()
    capital = StringField()
    countinent = StringField()
    tld = StringField()
    currency_code = StringField()
    currency_name = StringField()
    phone = StringField()
    postal_code_format = StringField()
    postal_code_regex = StringField()
    langs = StringField()
    neighbours = StringField()

    updated = BooleanField(default=False)




if __name__ == '__main__':
    print Proxy.get_random_proxy()