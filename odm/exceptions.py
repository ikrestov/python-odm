#! /usr/bin/python

__author__="Igor Kretov"
__date__ ="$23-Jul-2012 21:47:09$"

class FieldException(Exception):
    pass

class InvalidException(FieldException):
    pass

class NotDefinedException(FieldException):
    pass