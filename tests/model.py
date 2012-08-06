#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$06-Aug-2012 08:45:19$"

import unittest
from odm import Model, IntegerField

class TestModel(Model):
    int_field = IntegerField()
    manager_send = 'THIS IS PASSED TO MANAGER'

    class Meta:
        pk_name = '_id'
        pass_to_manager = ('manager_send',)
            
class ModelTestCase(unittest.TestCase):
    pk_name = '_id'
                    
    def setUp(self):
        self.baseModelClass = TestModel
        self.baseModelObj = TestModel()
        
    def test_meta_config_set(self):
        self.assertEqual(self.baseModelObj.Meta.pk_name, self.pk_name)
        
    def test_meta_config_default(self):
        self.assertEqual(self.baseModelObj.Meta.strict, Model.Meta.strict)
        
    def test_field_exists(self):
        self.assertTrue('int_field' in self.baseModelObj._fields)
        self.assertTrue('int_field' in self.baseModelObj._default)
        
    def test_field_name(self):
        self.assertTrue(getattr(self.baseModelObj, 'int_field').field_name, 'int_field')
        
    def test_manager_exists(self):
        self.assertTrue('objects' in self.baseModelObj._managers)
        
    @unittest.skipIf('pass_to_manager' not in TestModel.Meta.__dict__)
    def test_manager_pass(self):
        for attr in self.baseModelObj.Meta.pass_to_manager:
            self.assertEqual(getattr(self.baseModelObj.objects, attr), getattr(self, attr))
        
    def test_manager_model(self):
        self.assertEqual(self.baseModelObj.objects.model_class, self.baseModelClass)
