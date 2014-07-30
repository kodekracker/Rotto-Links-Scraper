#! /usr/bin/env python
# -*- coding : utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import BINARY
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import JSONType

from jsonserializer import JsonSerializer

Base = declarative_base()

# Declare all required classes for database
class Website(Base):
    __tablename__ = 'website'
    id = Column(BINARY(16), primary_key=True)
    url = Column(String(100), nullable=False)
    last_time_crawled = Column(DateTime, default=func.now())
    status = Column(String(10), nullable=False)
    keywords = Column(String(500), nullable=False)
    result = Column(JSONType)
    user_id = Column(BINARY(16), ForeignKey('user.id', ondelete='CASCADE'))
    def __repr__(self):
        return '( Website: {0.url} - {0.last_time_crawled} - {0.status} - {0.keywords} - {0.result} )'.format(self)

class User(Base):
    __tablename__ = 'user'
    id = Column(BINARY(16), primary_key=True)
    email_id = Column(String(50), nullable=False)
    websites = relationship("Website", backref='user', cascade="all, delete-orphan", passive_deletes=True)
    def __repr__(self):
        return '( User: {0.email_id} )'.format(self)

# JsonSerializer classess
class UserWebsiteJsonSerializer(JsonSerializer):
    __attributes__ = ['id','url','keywords','status','last_time_crawled']
    __required__ = ['id','url','keywords','status']
    __attribute_serializer__ = dict(id='id', last_time_crawled='date', keywords='keywords')
    __object_class__ = Website
    def __init__(self):
        super(UserWebsiteJsonSerializer, self).__init__()
        self.serializers['keywords'] = dict(
            serialize=lambda x: x.split(','),
            deserialize=lambda x: ','.join(x)
        )

class UserJsonSerializer(JsonSerializer):
    __attributes__ = ['id', 'email_id', 'websites']
    __required__ = ['id','email_id']
    __attribute_serializer__ = dict(id = 'id', websites='websites')
    __object_class__ = User
    def __init__(self):
        super(UserJsonSerializer, self).__init__()
        self.serializers['websites'] = dict(
            serialize=lambda x:
                [UserWebsiteJsonSerializer().serialize(xx) for xx in x],
            deserialize=lambda x:
                [UserWebsiteJsonSerializer().deserialize(xx) for xx in x]
        )

class WebsiteUserJsonSerializer(JsonSerializer):
    __attributes__ = ['id', 'email_id']
    __required__ = ['id', 'email_id']
    __attribute_serializer__ = dict(id='id')
    __object_class__ = User
    def __init__(self):
        super(WebsiteUserJsonSerializer, self).__init__()

class WebsiteJsonSerializer(JsonSerializer):
    __attributes__ = ['id', 'url', 'last_time_crawled', 'status','keywords','result', 'user']
    __required__ = ['id','url','keywords','status']
    __attribute_serializer__ = dict(id='id', last_time_crawled='date', user='user', keywords='keywords')
    __object_class__ = Website

    def __init__(self):
        super(WebsiteJsonSerializer, self).__init__()
        self.serializers['keywords'] = dict(
            serialize=lambda x: x.split(','),
            deserialize=lambda x: ','.join(x)
        )
        self.serializers['user'] = dict(
            serialize=lambda x: WebsiteUserJsonSerializer().serialize(x),
            deserialize=lambda x: WebsiteUserJsonSerializer().deserialize(x)
        )
