#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$24-Jul-2012 23:12:41$"

class Manager(object):
    """
    **Abstract** object Manager class, set as a model's attribute (default *objects*)
    """
    def __init__(self, model_class=None):
        self.set_model_class(model_class)
        
    def set_model_class(self, model_class):
        """
        Functions checks passed *model_class*, and sets it *private* attribute.
        """
        #if not issubclass(model_class, Model):
        #    raise Exception('Passed model class', model_class, 'is not subclass of base Model')
        self._model_class = model_class
        
    def create(self):
        """
        Creates, validates, saves Model, and returns it's instance
        """
        raise NotImplementedError()
    
    def get(self):
        """
        Function fetches/ loads only **one** record, returns instance of class *Model*
        """
        raise NotImplementedError()
    
    def filter(self):
        """
        Theoretical function for filtering objects on application logic's level. 
        Returns *Iterable*
        **Optional**
        """
        raise NotImplementedError() # Should return iterable
    
    def fetch(self):
        """
        Loads a list of objects, returns *Iterable*.
        Each value is instance of class *Model*.
        """
        raise NotImplementedError() # Should return iterable

# Prevents recursive import
from .models import Model