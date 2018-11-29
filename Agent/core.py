# -*- coding: utf-8 -*-

"""

"""
import helpers
from Classes.Test import Test

def start():
    """Start the App"""
    if helpers.getAnswer():
        print(Test.getHmm())
