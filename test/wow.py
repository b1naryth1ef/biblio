"""
This is a test module
"""
from os import path
import os

CONSTANT_A = 1
CONSTANT_B = 'wow!'

def my_api_function(arga, argb, argc):
    """
    A function which does things when called.

    Paramaters
    ----------
    arga : int
        First argument to the function
    argb : `NonExistantClass`
        Second argument to the function
    argc : `TestClass`
        Third argument to the function

    Raises
    ------
    `ArgumentError`
        If shit is fucked

    Returns
    -------
    int
        The result of the function
    """
    pass


class TestClass(object):
    """
    A class which helps do things.
    """
    attribute = 1

    @property
    def test_property(self):
        """
        A test property
        """
        return 1

    @staticmethod
    def static_method(a, b, c):
        """
        A test static method
        """
        return a * b * c

    @classmethod
    def class_method(cls, a, b, c):
        """
        A test class method
        """
        return cls(a * b * c)

    def method(self, a, b, c=1, *args, **kwargs):
        """
        A test method
        """
        return a * b * c
