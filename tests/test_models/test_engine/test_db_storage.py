#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """test get method"""
        new = State(name="Holberland")
        new.save()
        self.assertIs(models.storage.get("State", new.id), new)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """ Test count """
        my_initial_count = storage.count(State)
        new_state = State(name="Antioquia")
        new_state.save()
        my_new_count = storage.count(State)
        self.assertTrue((my_initial_count + 1) == my_new_count)


class TestDBStorageMethod(unittest.TestCase):
    """Test the DBStorage class methods"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    @classmethod
    def setUpClass(cls):
        """Creating the objects to use"""
        cls.object_state = State(name="California")
        cls.object_city = City(state_id=cls.object_state.id,
                               name="Los Angeles")
        cls.object_state.save()
        cls.object_city.save()

    @classmethod
    def tearDownClass(cls):
        """ test """
        models.storage.delete(cls.object_state)
        models.storage.delete(cls.object_city)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """ test the get method for an existing object of class cls  """
        first_state_id = list(models.storage.all(State).values())[0].id
        answ = models.storage.get(State, first_state_id)
        self.assertEqual(answ.__class__.__name__, "State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """ test """
        answ = models.storage.count()
        self.assertEqual(answ, 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_cls(self):
        """ test """
        answ = models.storage.count(State)
        self.assertEqual(answ, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_None_cls(self):
        """ test """
        answ = models.storage.count(Review)
        self.assertEqual(answ, 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_db_storage(self):
        """Test"""
        storage.reload()
        result = storage.all("")
        count = storage.count(None)
        self.assertEqual(len(result), count)
        result = storage.all("State")
        count = storage.count("State")
        self.assertEqual(len(result), count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_file_storage(self):
        """ test """
        fs = FileStorage()
        new_state = State()
        fs.new(new_state)
        first_state_id = list(storage.all("State").values())[0].id
        self.assertEqual(type(storage.get("State", first_state_id)), State)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        storage = FileStorage()
        length = len(storage.all())
        self.assertEqual(storage.count(), length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)
