#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$24-Jul-2012 23:12:41$"

class Manager(object):
    """
    **Abstract** object Manager class, set as a model's attribute (default *objects*)
    """
    def __init__(self, model_class=None):
        self._model_class=None
        self.model_class=model_class
        
    @property
    def model_class(self):
        """
        Getter for Manager's Model Class
        """
        return self._model_class
        
    @model_class.setter
    def model_class(self, model_class):
        """
        Functions checks passed *model_class*, and sets it *private* attribute.
        """
        if model_class is not None and not hasattr(model_class, '__call__'):
            raise Exception('Passed model class', model_class, 'is not callable')
        self._model_class = model_class

    def __getattr__(self, name):
        return getattr(self._model_class, name)
        
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
    
    def fetch(self):
        """
        Loads a list of objects, returns *Iterable*.
        Each value is instance of class *Model*.
        """
        raise NotImplementedError()

