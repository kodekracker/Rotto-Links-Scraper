#! /usr/bin/env python
# -*- coding : utf-8 -*-

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Declare association/linker classes for many-many relationships
class WebsiteUserLink(Base):
    __tablename__ = 'website_user_link'
    website_id = Column(Integer, ForeignKey('websites.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class WebsiteKeywordLink(Base):
    __tablename__ = 'website_keyword_link'
    website_id = Column(Integer, ForeignKey('websites.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)


class RottoPageKeywordLink(Base):
    __tablename__ = 'rottopage_keyword_link'
    rottopage_id = Column(Integer, ForeignKey('rottopages.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)


# Declare all required classes for database
class Website(Base):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    last_time_crawled = Column(DateTime, default=func.now())
    status = Column(String(10))
    rottopages = relationship("RottoPage", backref=backref("Website", uselist=True, passive_updates=False))
    keywords = relationship("Keyword", secondary=WebsiteKeywordLink.__tablename__, backref=backref("Website"))
    users = relationship("User", secondary=WebsiteUserLink.__tablename__, backref=backref("Website"))
    def __repr__(self):
        return '< {0}:{1.url}:{1.last_time_crawled}:{1.status}:{1.rottopages!r}:{1.keywords!r}:{1.users!r}>'.format(Website, self)


class RottoPage(Base):
    __tablename__ = 'rottopages'
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey('websites.id'))
    url = Column(String(100))
    rottourls = relationship("RottoUrl", backref=backref("BaseUrl", uselist=True, passive_updates=False))
    keywords = relationship("Keyword", secondary=RottoPageKeywordLink.__tablename__, backref=backref("RottoPage", uselist=True, passive_updates=False))
    def __repr__(self):
        return '<{0}:{1.url}:{1.rottourls!r}:{1.keywords!r}>'.format(RottoPage, self)


class RottoUrl(Base):
    __tablename__ = 'rottourls'
    id = Column(Integer, primary_key=True)
    rotto_page_id = Column(Integer, ForeignKey('rottopages.id'))
    url = Column(String(100))
    def __repr__(self):
        return '<{0}:{1.url}>'.format(RottoUrl, self)


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50))
    def __repr__(self):
        return '<{0}:{1.keyword}>'.format(Keyword, self)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email_id = Column(String(50))
    def __repr__(self):
        return '<{0}:{1.email_id}>'.format(User, self)
