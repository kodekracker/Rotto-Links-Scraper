#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from tests import test
from gui import app


if __name__ == '__main__':
    # set package path in system environmnet path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    sys.path.append(path)

    if(len(sys.argv)!=2):
        app.run()
    else:
        if(sys.argv[1]=='app'):
            app.run()
        elif(sys.argv[1]=='test'):
            test.run()

