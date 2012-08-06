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
    """
    Base Field class, contains base logic for type conversion and validation
    Override attribute *Field.type* to type (callable object which transforms passed argument into it's type) in **child classes**.
    """
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
        self.field_name = field_name
        self.default=default
        self.validate_function = validate if hasattr(validate, '__call__') else None
        if self.default is not None:
            self.validate(self.default)
        
    @classmethod
    def createByType(cls, type, *args, **kwargs):
        """
        Shortchut for creating custom Field based on type.
        """
        if not hasattr(type, '__call__'):
            raise FieldException("Type {0} is not callable".format(type))
        try:
            name = kwargs.pop('__name__')
        except KeyError:
            name = cls.__name__
        return type(name, (cls,), dict(type=type))()
        
    def validate(self, value=None):
        """
        Function performs type conversion and validation (if specified) on passed argument.
        """
        if value is not None:
            value = self.transform(value)
            if self.validate_function:
                valid, msg = self.validate_function(value)
                if not valid:
                    raise InvalidException(msg)
        elif self.required:
            raise NotDefinedException("Key {0} is not defined".format(self.field_name))
        return True
    
    def transform(self, value=None):
        """
        Performs Python type conversion, validation
        """
        try:
            return self._setter(value)
        except Exception as e:
            raise ValueError(*e.args)
        
    @property
    def field_name(self):
        """
        Getter for Field's name
        """
        return self._field_name
    
    @field_name.setter
    def field_name(self, name):
        """
        Setter function to set *Field*'s name.
        Called from Model's **Metaclass.__new__**.
        """
        if self._field_name is None:
            self._field_name = name

class IntegerField(Field):
    """Base IntegerField"""
    type=int
    
class FloatField(Field):
    """Base FloatField"""
    type=float

class DecimalField(Field):
    """Base DecimalField"""
    type=Decimal
       
class StringField(Field):
    """Base StringField"""
    type=str

class DatetimeField(Field):
    """Base DatetimeField"""
    type=datetime.datetime
    
    def _setter(self, value):
        if not isinstance(value, self.type): raise ValueError("{0} is not {1}".format(value, self.type))
        return value
    
class DateField(DatetimeField):
    """Base DateField"""
    type=datetime.date
        
class TimeField(DatetimeField):
    """Base TimeField"""
    type=datetime.time
    
