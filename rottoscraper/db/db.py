#! /usr/bin/env python
# -*- coding : utf-8 -*-

import uuid
import time
from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .models import Website
from .models import User
from .models import UserJsonSerializer
from .models import WebsiteJsonSerializer
from logger import log
from config import DATABASE_URI

# Create an engine that stores data file in the local directory's
engine = create_engine(DATABASE_URI, echo=False)

# Define a Session class which will serve as a factory for new Session objects
Session = sessionmaker(bind=engine)

s = Session()

class Status(Enum):
    PENDING='pending'
    QUEUED='queued'
    STARTED='started'
    FINISHED='finished'
    FAILED='failed'

def get_new_id(string, bytes=True, hex=False):
    """
    Returns a uuid in different format(i.e bytes/hex)
    """
    try:
        temp = str(time.time())
        string = string + temp
        sha1 = uuid.uuid5(uuid.NAMESPACE_URL, string.encode('utf-8'))

        if bytes:
            return sha1.bytes
        else:
            return sha1.hex
    except Exception:
        log.exception('Error in get new id')

def deserialize_id(id):
    """
    Deserialize the id(i.e hex to bytes)
    """
    return uuid.UUID(hex=id).bytes

class Database(object):

    @classmethod
    def create(cls):
        """
        Create all tables in the engine. This is equivalent to "Create Table"
        statements in raw SQL.
        """
        try:
            log.info('DB_URI :: {0} created'.format(DATABASE_URI))
            Base.metadata.create_all(engine)
        except Exception:
            log.exception('Error in creating database')

    @classmethod
    def website_exists(cls, url=None, id=None):
        """
        Tells whether website exists in db or not
        """
        try:
            if url:
                if(s.query(Website).filter(Website.url==url).count()>0):
                    return True
                else:
                    return False
            elif id:
                if(s.query(Website).filter(Website.id==deserialize_id(id)).count()>0):
                    return True
                else:
                    return False
            else:
                return False
        except Exception:
            log.exception('Error in website exists')

    @classmethod
    def user_exists(cls, email_id=None, id=None):
        """
        Tells whether user exists in db or not
        """
        try:
            if email_id:
                if(s.query(User).filter(User.email_id==email_id).count()>0):
                    return True
                else:
                    return False
            elif id:
                if(s.query(User).filter(User.id==deserialize_id(id)).count()>0):
                    return True
                else:
                    return False
            else:
                return False
        except Exception:
            log.exception('Error in user exists')

    @classmethod
    def fetch_website(cls, id=None, serialize=True):
        """
        Returns the website depends upon serialize variable.
        if true it returns website in json format otherwise
        a website identity object
        """
        try:
            website = s.query(Website).filter(Website.id==deserialize_id(id)).first()

            if serialize:
                website_json = WebsiteJsonSerializer().serialize(website)
                return website_json
            else:
                return website

        except Exception:
            log.exception('Error in fetch website')

    @classmethod
    def fetch_user(cls, id=None, email_id=None, serialize=True):
        """
        Returns the user depends upon serialize variable.
        if true it returns user in json format otherwise
        a user identity object
        """
        try:
            user = None
            if id:
                user = s.query(User).filter(User.id==deserialize_id(id)).first()
            else:
                user = s.query(User).filter(User.email_id==email_id).first()

            if serialize:
                user_json = UserJsonSerializer().serialize(user)
                return user_json
            else:
                return user
        except Exception:
            log.exception('Error in fetch user')

    @classmethod
    def add_request(cls, request):
        """
        Add website and user in db to process
        """
        try:
            user = None
            if not Database.user_exists(email_id=request['email_id']):
                user_id = get_new_id(request['email_id'])
                # create user identity object and save to db
                user = User(id=user_id, email_id=request['email_id'])
                s.add(user)
                s.commit()
            else:
                user = Database.fetch_user(email_id=request['email_id'], serialize=False)

            # create website identity object and save to db
            website_id = get_new_id(request['url'])
            website = Website(id=website_id, url=request['url'])
            website.keywords = ','.join(request['keywords'])
            website.status = Status.PENDING
            website.user = user
            s.add(website)
            s.commit()
            log.info('Add Request :: {0} :: {1}'.format(website.url, user.email_id))
            return WebsiteJsonSerializer().serialize(website)
        except Exception:
            log.exception('Error in add request')

    @classmethod
    def set_website_status(cls, id=None, status=Status.PENDING, result=None):
        """
        Set status and result of the website
        """
        try:
            website = s.query(Website).filter(Website.id==deserialize_id(id)).first()
            website.status = status
            print 'Setting status to {0} of {1}'.format(status, website.url)

            if result:
                website.result = result
            s.commit()
        except Exception:
            log.exception('Error in set website status')

    @classmethod
    def fetches(cls, limit=3):
        """
        Returns a list of websites having status pending
        """
        try:
            result = []
            websites = s.query(Website).filter(Website.status==Status.PENDING).limit(limit).all()
            if websites:
                for website in websites:
                    result.append(WebsiteJsonSerializer().serialize(website))
            return result
        except Exception:
            log.exception('Error in fetches')
