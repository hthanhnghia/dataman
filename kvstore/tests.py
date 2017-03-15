import unittest
import time
from django.test import TestCase
from mock import patch, Mock
from .key_value_storage import KeyValueStorage, InvalidTimestampException, NotFoundException
from .redis_client import redis_client
from .utils import lower_bound

mock_time = Mock()

class TestUtils(unittest.TestCase):
    def test_lower_bound_with_empty_arr(self):
        self.assertEqual(lower_bound([], 3), None)

    def test_lower_bound_with_val_less_than_min_array(self):
        self.assertEqual(lower_bound([1, 2.5, 5], 0.5), None)

    def test_lower_bound_with_val_equal_min_array(self):
        self.assertEqual(lower_bound([1, 2.5, 5], 1), 1)

    def test_lower_bound_with_val_between_max_and_min_array(self):
        self.assertEqual(lower_bound([1, 2.5, 5], 3), 2.5)

    def test_lower_bound_with_val_equal_max_array(self):
        self.assertEqual(lower_bound([1, 2.5, 5], 5), 5)

    def test_lower_bound_with_val_larger_than_max_array(self):
        self.assertEqual(lower_bound([1, 2.5, 5], 8.3), 5)

class TestKeyValueStorage(unittest.TestCase):
    def setUp(self):
        redis_client.flushall()
        self.key_value_storage = KeyValueStorage()

    def test_get(self):
        self.key_value_storage.save('key', 'value')
        self.assertEqual(self.key_value_storage.get('key', None), 'value')
    
    @patch('time.time', mock_time)
    def test_get_with_timestamp(self):
        mock_time.return_value = 1.5
        self.key_value_storage.save('key', 'value')
        self.assertEqual(self.key_value_storage.get('key', 2), 'value')

    def test_get_with_invalid_key(self):
        with self.assertRaises(NotFoundException):
            self.assertRaises(NotFoundException, self.key_value_storage.get('key'))

    def test_get_with_invalid_timestamp(self):
        self.key_value_storage.save('key', 'value')
        with self.assertRaises(InvalidTimestampException):
            self.assertRaises(InvalidTimestampException, self.key_value_storage.get('key', 'abc'))
        
class APIViewTestCase(TestCase):
    def setUp(self):
        redis_client.flushall()
        self.storage = KeyValueStorage()
    
    def test_save_value_for_key_success(self):
        response = self.client.post('/object', data = {'key': 'value'})
        self.assertEqual(response.content, 'The data has been added')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.storage.get('key'), 'value')
    
    def test_save_value_for_key_with_data_having_more_than_one_key(self):
        response = self.client.post('/object', data = {'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(response.content, 'Invalid request')
        self.assertEqual(response.status_code, 400)

    def test_save_value_for_key_with_invalid_data(self):
        response = self.client.post('/object', data = {"key"}, content_type='text/xml')
        self.assertEqual(response.content, 'Invalid request')
        self.assertEqual(response.status_code, 400)

    def test_get_value_by_key(self):
        self.storage.save('key', 'value')
        response = self.client.get('/object/key')
        self.assertEqual(response.content, 'value')
        self.assertEqual(response.status_code, 200) 

    @patch('time.time', mock_time)
    def test_get_value_by_key_and_timestamp(self):
        mock_time.return_value = 1.5
        self.storage.save('key', 'value')

        response = self.client.get('/object/key?timestamp=2')
        self.assertEqual(response.content, 'value')
        self.assertEqual(response.status_code, 200)

    def test_get_value_by_key_with_invalid_timestamp(self):
        response = self.client.get('/object/key?timestamp=abc')
        self.assertEqual(response.content, 'Invalid timestamp format - Timestamp must be a float')
        self.assertEqual(response.status_code, 400)     

    def test_get_value_by_key_with_non_existent_key(self):
        response = self.client.get('/object/key')
        self.assertEqual(response.content, '')
        self.assertEqual(response.status_code, 204)