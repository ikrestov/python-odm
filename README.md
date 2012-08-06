python-odm
==========

Simple Object Data Mapping library in Python

TESTS
-----

To run tests use one of:
```bash
python -m unittest tests.model 		# Just Python
python -m tornado.testing tests.model 	# If you are using Tornado
trial tests.model 			# If you are using Twisted
```

EXAMPLE
-------

```python
class MyModel(Model):
    objects = MyManager()
    field = IntegerField()

    def save(self, *args):
        # Your save logic
        pass

mytest = MyModel()
mytest['data'] = 123
try: mytest['field'] = 'Nil' # Raises exception
except ValueError as e: print(e)

print(mytest.model_to_dict())
```

TODO
----

* Description
* ~~Unit tests~~
* ~~Examples~~
