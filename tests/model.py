#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$06-Aug-2012 08:45:19$"

import unittest
from odm import Model, IntegerField

class TestModel(Model):
    int_field = IntegerField(default=0)
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
        
    @unittest.skipIf('pass_to_manager' not in TestModel.Meta.__dict__, "Meta.`pass_to_manager` is not set")
    def test_manager_pass(self):
        for attr in self.baseModelObj.Meta.pass_to_manager:
            self.assertEqual(getattr(self.baseModelObj.objects, attr), getattr(self.baseModelClass, attr))
        
    def test_manager_model(self):
        self.assertEqual(self.baseModelObj.objects.model_class, self.baseModelClass)
        
    def test_model_to_dict(self):
        self.baseModelObj['int_field']=1
        self.assertEqual(self.baseModelObj.model_to_dict()['int_field'], 1)
        
    def test_model_from_dict(self):
        m = self.baseModelClass.model_from_dict({'int_field': 1})
        self.assertEqual(m['int_field'], 1)
    
    def test_model_from_dict_fail(self):
        with self.assertRaises(ValueError):
            self.baseModelClass.model_from_dict({'int_field': 'NOT STIRNG'})
 
    def test_field_validation(self):
        with self.assertRaises(ValueError):
            self.baseModelObj['int_field']='string'
            self.baseModelObj.model_to_dict()
            
    def test_model_strict(self):
        class StrictModel(self.baseModelClass):
            class Meta:
                strict = True
                
        m = StrictModel()
        with self.assertRaises(m.Invalid):
            m['undefined_field']=True

    def test_model_strict_load_fail(self):
        class StrictModel(self.baseModelClass):
            class Meta:
                strict = True
        with self.assertRaises(StrictModel.Invalid):
            StrictModel.model_from_dict({'field': 'STIRNG'})
            
    def test_model_required(self):
        class RequiredModel(self.baseModelClass):
            int_field = IntegerField(required=True)
        
        m = RequiredModel()
        with self.assertRaises(m.NotDefined):
            m.model_to_dict()
        
