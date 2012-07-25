#! /usr/bin/python

###
#
# TODO = Complex Field (Lists/Hash/Sets (with primitives/ComplexFields inside)
###

__author__="Igor Krestov"
__date__ ="$23-Jul-2012 21:43:00$"

from .exceptions import FieldException, InvalidException, NotDefinedException
from decimal import Decimal
import datetime

class Field(object): 
    type = None
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_setter'):
            if cls.type is not None and hasattr(cls.type, '__call__'):
                # THIS IS BAD TRANSFORMATION
                # BULSHITTT
                # lambda s,v: isinstance(v, cls.type) and v
                cls._setter = lambda s, v: cls.type(v)
            else:
                cls._setter = lambda s, v: v
        inst = super(Field, cls).__new__(cls, *args, **kwargs)
        return inst
        
    def __init__(self, required=False, validate=None, default=None, field_name=None):
        self.required = required
        self._field_name = field_name
        self.default=default
        self.validate_function = validate if hasattr(validate, '__call__') else None
        if self.default is not None:
            self.validate(self.default)
        
    @classmethod
    def createByType(cls, type, *args, **kwargs):
        if not hasattr(type, '__call__'):
            raise FieldException("Type {0} is not callable".format(type))
        try:
            name = kwargs.pop('__name__')
        except KeyError:
            name = cls.__name__
        return type(name, (cls,), dict(type=type))()
        
    def validate(self, value=None):
        if value is not None:
            value = self.transform(value)
            if self.validate_function:
                valid, msg = self.validate_function(value)
                if not valid:
                    raise InvalidException(msg)
        elif self.required:
            raise NotDefinedException("Key {0} is not defined".format(self._field_name))
        return True
    
    def transform(self, value=None):
        try:
            return self._setter(value)
        except Exception as e:
            raise ValueError(*e.args)
        
    def set_field_name(self, name):
        if self._field_name is None:
            self._field_name = name

class IntegerField(Field):
    type=int
    
class FloatField(Field):
    type=float

class DecimalField(Field):
    type=Decimal
       
class StringField(Field):
    type=str

class DatetimeField(Field):
    type=datetime.datetime
    
    def _setter(self, value):
        if not isinstance(value, self.type): raise ValueError("{0} is not {1}".format(value, self.type))
        return value
    
class DateField(DatetimeField):
    type=datetime.date
        
class TimeField(DatetimeField):
    type=datetime.time
    
