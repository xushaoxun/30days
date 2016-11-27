# coding:utf-8
from mongoengine import connect, StringField, DateTimeField, Document, DoesNotExist, DictField, IntField, ListField
from mongoengine.fields import ReferenceField
from config import DB_HOST, DB_PORT, DATABASE_NAME
import datetime

connect(DATABASE_NAME, host=DB_HOST, port=DB_PORT)

class BaseModel(Document):
    create_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'allow_inheritance':True,
        'abstract': True,
    }

class Proxy(BaseModel):
    address = StringField(unique=True)

    # meta = {'collection': 'proxy'}

    @classmethod
    def get_random_proxy(cls):
        '''
        use ['address']
        :return:
        '''
        proxy = cls.objects.aggregate({'$sample': {'size': 1}}).next()
        return proxy

    @classmethod
    def del_proxy(cls, address):
        try:
            Proxy.objects.get(address=address).delete()
        except DoesNotExist:
            pass


class Publisher(BaseModel):
    display_name = StringField(max_length=50, required=True)

    meta = {'collection': 'publisher'}

    @classmethod
    def get_or_create(cls, display_name):
        try:
            return cls.objects.get(display_name=display_name)
        except DoesNotExist:
            publisher = cls(display_name=display_name)
            publisher.save()
            return publisher


class Article(BaseModel):
    title = StringField(max_length=120, required=True)
    img_url = StringField()
    url = StringField(required=True, unique=True)
    summary = StringField()
    publisher = ReferenceField(Publisher, required=True)

    content = StringField()
    pictures = DictField()
    read_num = IntField()
    like_num = IntField()
    comments = ListField(ReferenceField('Comment'))

    meta = {
        # 'collection': 'article',
        'indexes': [
            '-create_at',
            {'fields': ['title', 'publisher'], 'unique': True},
        ],
        'ordering': ['-create_at']
    }

class Comment(BaseModel):
    nickname = StringField(max_length=32)
    content = StringField(required=True)
    like_num = IntField()
    comment_id = IntField()
    article = ReferenceField('Article', dbref=True)

    meta = {
        'indexs': [
            {'fields': ['article', 'comment_id'], 'unique':True}
        ]
    }

    @classmethod
    def get_or_create(cls, article, comment_id, **kwargs):
        comments = cls.objects.filter(article=article, comment_id=comment_id)

        if comments:
            return comments[0]

        comment = cls(article=article, comment_id=comment_id, **kwargs)
        comment.save()
        return comment


if __name__ == '__main__':
    print Proxy.get_random_proxy()