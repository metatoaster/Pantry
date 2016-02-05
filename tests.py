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

if __name__ == '__main__':
    unittest.main()
