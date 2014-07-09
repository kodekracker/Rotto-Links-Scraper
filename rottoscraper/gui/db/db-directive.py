


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, \
	ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class HostUrl(Base):

	__tablename__ = 'hosturl'

	id = Column(Integer, primary_key=True)
	url = Column(String(100))
	last_time = Column(DateTime)

	def __repr(self):
		return "<HostUrl(url='%s', last_time='%s')>" % \
		(self.url, self.last_time)

class BaseUrl(Base):

	__tablename__ = 'baseurl'

	id = Column(Integer, primary_key=True)
	host_url_id = Column(String, ForeignKey('hosturl.id'))
	url = Column(String(100))

	def __repr(self):
		return "<BaseUrl(host_url_id='%s', url='%s')>" % \
		(self.host_url_id, self.url)


class RottoUrl(Base):

	__tablename__ = 'rottourl'

	id = Column(Integer, primary_key=True)
	base_url_id = Column(String, ForeignKey('baseurl.id'))
	url = Column(String(100))

	def __repr(self):
		return "<RottoUrl(base_url_id='%s', url='%s')>" % \
		(self.url)

class MatchKeyword(Base):

	__tablename__ = 'matchkeyword'

	id = Column(Integer, primary_key=True)
	base_url_id = Column(String, ForeignKey('baseurl.id'))
	keyword = Column(String(50) )

	def __repr(self):
		return "MatchKeyword<keyword='%s')>" % \
		(self.keyword)


engine =  create_engine('sqlite:///linkscaper.db')

Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)

