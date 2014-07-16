#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class ContentTypeError(Error):
    """Raised when the content type of response is not text/html"""
    pass
