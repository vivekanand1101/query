import math
import json
import unittest

import server
from server import SEARCH_LEN, binsearch, edit_distance

EXPECTED_SEARCH_OUTPUTS = {
    'rohit': ['rohitwilliam', 'rohityadav', 'rohiy', 'rohiya', 'rohnit',
                'rohon', 'rohonikumar', 'rohot', 'rohtas', 'rohtash'],
}

EXPECTED_JSON_OUTPUTS = {
    'rohit': {
        u"results": [
            {
                u"name": u"rohityadav",
                u"score": u"matching"
            },
            {
                u"name": u"rohitwilliam",
                u"score": u"matching"
            },
            {
                u"name": u"rohiy",
                u"score": 1
            },
            {
                u"name": u"rohot",
                u"score": 1
            },
            {
                u"name": u"rohnit",
                u"score": 1
            },
            {
                u"name": u"rohon",
                u"score": 2
            },
            {
                u"name": u"rohiya",
                u"score": 2
            },
            {
                u"name": u"rohtas",
                u"score": 3
            },
            {
                u"name": u"rohtash",
                u"score": 4
            },
            {
                u"name": u"rohonikumar",
                u"score": 7
            },
        ]
    },
    'A': {
        "results": [],
    }
}

class TestServer(unittest.TestCase):
    ''' Tests Methods of server.py '''

    def setUp(self):
        ''' Setup the test suite, only necessary for flask views '''
        server.app.testing = True
        self.app = server.app.test_client()
        self.maxDiff = None

    def test_binsearch(self):
        ''' Test the binsearch method of server module '''
        output = binsearch('rohit')
        self.assertEqual(output, EXPECTED_SEARCH_OUTPUTS['rohit'])

        # check if number of outputs is less than or equal to SEARCH_LEN
        self.assertTrue(len(output) <= SEARCH_LEN)

    def test_edit_distance(self):
        ''' Test the edit_distance method of server module '''
        output = edit_distance('A', 'A')
        self.assertEqual(output, 0)

        # check for outputs when the given_str starts with target_str
        output = edit_distance('AA', 'A')
        self.assertTrue(math.isinf(output))

    def test_hello_world(self):
        ''' Test the hello_world view of the server module '''
        output = self.app.get('/auto?q=rohit')

        # check status code
        self.assertEqual(output.status_code, 200)
        # check the json output
        self.assertEqual(json.loads(output.data), EXPECTED_JSON_OUTPUTS['rohit'])

        # length of query string is < 3
        output = self.app.get('/auto?q=A')
        self.assertEqual(json.loads(output.data), EXPECTED_JSON_OUTPUTS['A'])

if __name__ == '__main__':
    unittest.main()
