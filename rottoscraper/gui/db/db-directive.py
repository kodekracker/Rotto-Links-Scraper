#! /usr/bin/env python
# -*- coding : utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HostUrl(Base):

	__tablename__ = 'hosturl'

	id = Column(Integer, primary_key=True)
	url = Column(String(100))
	last_time_crawled = Column(DateTime)

	def __repr__(self):
		return "<HostUrl(url='%s', last_time='%s')>" % (self.url, self.last_time)


class BaseUrl(Base):

	__tablename__ = 'baseurl'

	id = Column(Integer, primary_key=True)
	host_url_id = Column(String, ForeignKey('hosturl.id'))
	url = Column(String(100))

	def __repr__(self):
		return "<BaseUrl(host_url_id='%s', url='%s')>" % (self.host_url_id, self.url)


class RottoUrl(Base):

	__tablename__ = 'rottourl'

	id = Column(Integer, primary_key=True)
	base_url_id = Column(String, ForeignKey('baseurl.id'))
	url = Column(String(100))

	def __repr__(self):
		return "<RottoUrl(base_url_id='%s', url='%s')>" % (self.url)


class MatchedKeyword(Base):

	__tablename__ = 'matchedkeyword'

	id = Column(Integer, primary_key=True)
	base_url_id = Column(String, ForeignKey('baseurl.id'))
	keyword = Column(String(50) )

	def __repr__(self):
		return "MatchedKeyword<keyword='%s')>" % (self.keyword)


engine =  create_engine('sqlite:///rotto-scaper.db')

Base.metadata.create_all(engine)
