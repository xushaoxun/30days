# coding:utf-8
import mongoengine, datetime
from mongoengine import Document, connect, ValidationError, DoesNotExist,QuerySet,\
    MultipleObjectsReturned, IntField, DateTimeField, StringField, SequenceField,\
    ReferenceField, URLField, ListField, EmbeddedDocument, EmbeddedDocumentField,\
    CASCADE, GenericReferenceField

conn = connect(host='mongodb://localhost/runoob')
# conn = connect('runoob')

class User(Document):
    email = StringField(required=True, unique=True)
    first_name = StringField(max_length=20)
    last_name = StringField(max_length=20)
    created = DateTimeField(default=datetime.datetime.now())

    meta = {
        'indexes': [
            'first_name',
            '$first_name',  # text index
            ('first_name', '-last_name'),
        ]
    }


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=100, required=True)
    # one to one
    author = ReferenceField(User, reverse_delete_rule=CASCADE)  #delete post if user is delete
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {
        'allow_inheritance': True,
        'abstract': True
    }

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    img_path = URLField()

class LinkPost(Post):
    link_url = URLField()

class Bookmark(Document):
    bookmark_obj = GenericReferenceField()

User.drop_collection()

rose = User(email='rose@qq.com', first_name='Rose', last_name='Lawly')
john = User(email='john@qq.com')
john.first_name = 'John'
john.last_name = 'Smith'
try:
    john.save()
    rose.save()
except mongoengine.errors.NotUniqueError as e:
    print e

john = User.objects.get(email='john@qq.com')
rose = User.objects.get(email='rose@qq.com')
rose.created= datetime.datetime.now()
rose.save()

post1 = TextPost(title='Fun with mongoengine', author=rose)
post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
post1.tags = ['mongo', 'mongoengine']
cmt = Comment(content='some comment')
post1.comments.append(cmt)
post1.save()

bookmark = Bookmark(bookmark_obj=post1).save()

#
post2 = LinkPost(title='MongoEngine Documentation', author=john)
post2.link_url = 'http://www.baidu.com'
post2.tags = ['baidu']
post2.save()
bookmark = Bookmark(bookmark_obj=post2).save()

# for t in TextPost.objects.all():
for t in TextPost.objects:
    print t.title

print '*'*100
for t in TextPost.objects(tags='mongo'):
    print t.title, t.comments

print '*'*100
for t in TextPost.objects(tags__0='mongo'):
    print t.title, t.comments

print '*'*100
TextPost.objects.order_by('title')

print TextPost.objects(title__contains='hello')