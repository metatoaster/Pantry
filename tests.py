import unittest
import tempfile
import os

from Pantry import pantry


class TestPantry(unittest.TestCase):

    def setUp(self):
        self.temp_file, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.temp_file)
        os.unlink(self.filename)

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

if __name__ == '__main__':
    unittest.main()
