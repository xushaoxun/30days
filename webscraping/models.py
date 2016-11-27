# coding:utf-8
from config import DB_URI
from mongoengine import StringField, connect, IntField, Document, DateTimeField, DoesNotExist
import datetime

connect(host=DB_URI)

class BaseModel(Document):
    create_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance': True,
        'abstract': True,
    }

class Proxy(BaseModel):
    address = StringField(required=True, unique=True)

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

if __name__ == '__main__':
    print Proxy.get_random_proxy()