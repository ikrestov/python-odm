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
    pk_name = 'id'
    
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if 'Meta' in attrs: attrs['Meta'] = type('Meta', (attrs['Meta'], ModelMeta), {})
        else: attrs['Meta'] = ModelMeta
        
        _default = {}
        _fields = {}
        for name, obj in attrs.iteritems():
            if isinstance(obj, Field):
                obj.set_field_name(name)
                if obj.default is not None:
                    _default[name] = obj.default
                _fields[name] = obj
        attrs['_fields'] = _fields
        attrs['_default'] = _default
        
        clsObject = super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)
        
        try: pass_to_manager = getattr(attrs['Meta'], 'pass_to_manager')
        except AttributeError: pass_to_manager = ()
        for obj in attrs.itervalues():
            if isinstance(obj, Manager):
                obj.set_model_class(clsObject)
                for name in pass_to_manager:
                    try:
                        setattr(obj, name, getattr(clsObject, name))
                    except:
                        pass
        
        return clsObject
            
class Model(object):
    __metaclass__ = ModelMetaClass
    
    Invalid = InvalidException
    NotDefined = NotDefinedException
    
    objects = Manager()
    #class ModelManager(Manager):
    #    pass
    
    #objects = ModelManager()

    def __init__(self, data):
        self.data = copy.deepcopy(self.__class__._default)
        self.data.update(data)
                
    @property
    def pk(self):
        return self.data.get(self.Meta.pk_name, None)
        
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

Manager.model_base_class = Model
