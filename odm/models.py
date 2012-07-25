#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$23-Jul-2012 22:59:05$"

from .exceptions import InvalidException, NotDefinedException
from .fields import Field
from .manager import Manager
import copy

class ModelMeta(object):
    lazy_validation = False
    strict = False
        
class Model(object):
    Invalid = InvalidException
    NotDefined = NotDefinedException
    
    objects = Manager()
    #class ModelManager(Manager):
    #    pass
    
    #objects = ModelManager()
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_fields'):
            cls._default = {}
            cls._fields = {}
            for name, obj in cls.__dict__.iteritems():
                cls._attribute_hook(name, obj)
        if hasattr(cls, 'Meta'):
            cls.Meta = type('Meta', (cls.Meta, ModelMeta), {})
        else:
            cls.Meta = ModelMeta
        return super(Model, cls).__new__(cls, *args, **kwargs)
         
    def __init__(self, **kwargs):
        self.data = copy.deepcopy(self.__class__._default)
        self.data.update(kwargs)
        
    @classmethod
    def _attribute_hook(cls, name, obj):
        if isinstance(obj, Field):
            obj.set_field_name(name)
            if obj.default is not None:
                cls._default[name] = obj.default
            cls._fields[name] = obj
        if isinstance(obj, Manager):
            obj.set_model_class(cls)
                    
    def validate_object(self):
        for name, field in self._fields.iteritems():
            field.validate(self.data.get(name))
            
    def validate_fields(self):
        for key in self.data.iterkeys():
            if key not in self._fields:
                raise self.Invalid("Model {0} is strict and key {1} is not defined".format(self.__class__.__name__, key))
        
    def model_to_dict(self):
        if self.Meta.strict:
            self.validate_fields()
        self.validate_object()
        return self.data
    
    @classmethod
    def model_from_dict(cls, data):
        inst = cls()
        inst.load(data)
        if inst.Meta.strict:
            inst.validate_fields()
        inst.validate_object()
        return inst
        
    def load(self, data):
        ## TODO = Refactoring/ Optimization
        if self.Meta.strict:
            self.data = copy.deepcopy(self.__class__._default)
            for key, value in data.iteritems():
                if key in self._fields:
                    self.data[key] = value
        else:
            self.data = copy.deepcopy(data)
        
    def save(self):
        raise NotImplementedError()
    
    def __setattr__(self, name, value):
        
        super(Model, self).__setattr__(name, value)
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        field = self._fields.get(key)
        if not self.Meta.lazy_validation:
            if hasattr(field, 'validate'):
                field.validate(value)
            elif self.Meta.strict:
                raise self.Invalid("Model {0} is strict and key {1} is not defined".format(self.__class__.__name__, key))
        if hasattr(field, 'transform'):
            self.data[key] = field.transform(value)
        else:
            self.data[key] = value
        
    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.iteritems()
    
    def __contains__(self, key):
        return key in self.data