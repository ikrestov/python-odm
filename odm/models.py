#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$23-Jul-2012 22:59:05$"

from .exceptions import InvalidException, NotDefinedException
from .fields import Field
from .manager import Manager
import copy
import collections

class ModelMeta(object):
    """
    Base class for Model behaviour configuration
    """
    lazy_validation = False
    strict = False
    pk_name = 'id'
    pass_to_manager = ()
    

class ModelMetaClass(collections.MutableMapping.__metaclass__):
    """
    Metaclass for class Model.
    Creates field list, sets name to field instances,
    configures Manager instance (sets Model class as attribute)
    """
    def __new__(cls, klasname, bases, attrs):
        ParentMeta = ModelMetaClass.collect_from_bases(bases, 'Meta', ModelMeta)
        if 'Meta' in attrs: attrs['Meta'] = type('Meta', (ParentMeta,), attrs['Meta'].__dict__)
        else: attrs['Meta'] = ParentMeta
        
        _default = ModelMetaClass.collect_from_bases(bases, '_default', {}, _copy=1)
        _fields = ModelMetaClass.collect_from_bases(bases, '_fields', {}, _copy=1)
        _managers = ModelMetaClass.collect_from_bases(bases, '_managers', {}, _copy=1)
        for name, obj in attrs.iteritems():
            if isinstance(obj, Field):
                obj.field_name=name
                if obj.default is not None:
                    _default[name] = obj.default
                elif name in _default:
                   del _default[name]
                _fields[name] = obj
            if isinstance(obj, Manager):
                _managers[name] = obj
        attrs['_fields'] = _fields
        attrs['_default'] = _default
        attrs['_managers'] = _managers
        attrs.update(_managers)
       
        clsObject = super(ModelMetaClass, cls).__new__(cls, klasname, bases, attrs)
        
        try: pass_to_manager = getattr(attrs['Meta'], 'pass_to_manager')
        except AttributeError: pass_to_manager = ()
          
        for manager in _managers.itervalues():
            manager.model_class=clsObject
            for name in pass_to_manager:
                try:
                    setattr(manager, name, getattr(cls, name))
                except AttributeError:
                    pass
        
        return clsObject 
    
    @staticmethod
    def collect_from_bases(bases, attr, default=None, _copy=0):
        attr_value = None
        for base in reversed(bases):
            try:
                attr_value = getattr(base, attr)
            except AttributeError:
                pass
        if attr_value is None:
            return default
        elif _copy > 0:
            if _copy > 1:
                return copy.deepcopy(attr_value)
            else:
                return copy.copy(attr_value)
        else:
            return attr_value
            
            
class Model(collections.MutableMapping):
    """
    Base class for your Models.
    Usage:
        class MyModel(Model)
            objects = MyManager()
            field = IntegerField()
            
            def save(self, *args):
                # Your save logic
                
        mytest = MyModel()
        mytest['data'] = 123
        mytest['field'] = 'wefwef' # Raises exception
        print(mytest.model_to_dict())
    """
    __metaclass__ = ModelMetaClass
    
    Invalid = InvalidException
    NotDefined = NotDefinedException
    
    objects = Manager()

    def __init__(self, data=None):
        if data is None:
            self.data = copy.deepcopy(self.__class__._default)
        else:
            self.data = data
            for name, val in self.__class__._default.iteritems():
                if name not in self.data:
                    self.data[name]=val
                    
                
    @property
    def pk(self):
        """
        Returns Primary Key identified by **Meta.pk_name**
        """
        return self.data.get(self.Meta.pk_name, None)
       
    @pk.setter
    def pk(self, value):
        """
        Sets Primary Key identified by **Meta.pk_name**
        """
        self.data[self.Meta.pk_name] = value
    
    def validate_object(self):
        """
        Validates object's existing fields.
        """
        for name, field in self._fields.iteritems():
            field.validate(self.data.get(name))
            
    def validate_fields(self):
        """
        Check for existance of fields for each key and raise exception if *key* is not in *fields*.
        """
        for key in self.data.iterkeys():
            if key not in self._fields:
                raise self.Invalid("Model {0} is strict and key {1} is not defined".format(self.__class__.__name__, key))
        
    def model_to_dict(self):
        """
        Validates model and returns dictionary of data.
        Should be used for *save()* method implementation.
        """
        if self.Meta.strict:
            self.validate_fields()
        self.validate_object()
        return self.data
    
    @classmethod
    def model_from_dict(cls, data):
        """
        *Class* method for validating dictionary and loading it into new Model instance.
        Raises validation exceptions.
        """
        inst = cls()
        inst.load(data)
        if inst.Meta.strict:
            inst.validate_fields()
        inst.validate_object()
        return inst
        
    def load(self, data):
        """
        Load and validate data from passed dictionary.
        **Warning!!! Deletes old data!**
        """
        ## TODO = Refactoring/ Optimization
        if self.Meta.strict:
            self.data = copy.deepcopy(self.__class__._default)
            for key, value in data.iteritems():
                if key in self._fields:
                    self.data[key] = value
        else:
            self.data = copy.deepcopy(data)
        
    def save(self):
        """
        Function for object *save* logic.
        **NotImplemented**
        """
        raise NotImplementedError()
    
    def delete(self):
        """
        Function for object *delete* logic.
        **NotImplemented**
        """
        raise NotImplementedError()
   
    @classmethod
    def set_attr(cls, name, value):
        setattr(cls, name, value)
        if name in cls.Meta.pass_to_manager:
            for manager in cls._managers.itervalues():
                setattr(manager, name, value)

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
        return iter(self.data)
    
    def iteritems(self):
        return self.data.iteritems()
    
    def __contains__(self, key):
        return key in self.data

