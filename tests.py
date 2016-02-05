import unittest
import tempfile
import os
import os.path

from pantry import pantry


class TestPantry(unittest.TestCase):

    def setUp(self):
        self.temp_file, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.temp_file)
        os.unlink(self.filename)


class TestPantryContext(TestPantry):

    def test_write_to_pantry(self):
        with pantry(self.filename) as p:
            self.assertEqual(isinstance(p, dict), True)  # pantry object should be dict

            p['Test'] = True  # write to pantry object

    def test_read_from_pantry(self):
        with pantry(self.filename) as p:
            self.assertEqual(isinstance(p, dict), True)  # pantry object should be dict
            p['Test'] = True  # write to pantry

        with pantry(self.filename) as q:
            self.assertEqual(q['Test'], True)  # Should be True
            q['SecondTest'] = 4  # determined to be random enough
            #q.pop('Test')

        with pantry(self.filename) as r:
            self.assertEqual(r['Test'], True)  # previous write
            self.assertEqual(r['SecondTest'], 4)  # second write

    def test_no_file_pantry(self):
        self.assertFalse(os.path.exists(self.filename+'new'))

        with pantry(self.filename+'new') as p:
            p['Test'] = True  # write to new pantry

        with pantry(self.filename+'new') as p:
            self.assertEqual(p['Test'], True)


class TestPantryClass(TestPantry):

    def test_new_pantry(self):
        p = pantry.open(self.filename)
        self.assertEqual(p.db, {}) # should be empty
        p.db['Test'] = True
        p.close()

        q = pantry.open(self.filename)
        self.assertTrue(q.db['Test'])

    def test_no_file_pantry(self):
        p = pantry.open(self.filename+'new')
        self.assertEqual(p.db, {}) # should be empty

class CustomPantry(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def do_math(self):
        return sum(self.args)

class TestPantryCustomClass(TestPantry):

    def test_pantry_custom_class(self):
        p = pantry.open(self.filename)
        custom = CustomPantry(True, False, a=1, b=2)
        p.db = custom
        self.assertEqual(p.db.kwargs['a'], 1)
        p.close()

        q = pantry.open(self.filename)
        self.assertEqual(q.db.kwargs['a'], 1)

    def test_pantry_custom_class_defs(self):
        p = pantry.open(self.filename)
        p.db = CustomPantry(1,2,3,4,5)
        self.assertEqual(sum(p.db.args), sum((1,2,3,4,5)))
        p.close()

        with pantry(self.filename) as q:
            self.assertEqual(p.db.do_math(), sum((1,2,3,4,5)))

if __name__ == '__main__':
    unittest.main()
