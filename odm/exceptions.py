#! /usr/bin/python

__author__="Igor Kretov"
__date__ ="$23-Jul-2012 21:47:09$"

class FieldException(Exception):
    """Base Field Exception"""
    pass

class InvalidException(FieldException):
    """Base Exception for Invalid data cases"""
    pass

class NotDefinedException(InvalidException):
    """Exception for cases when field is required, but is not defined"""
    pass