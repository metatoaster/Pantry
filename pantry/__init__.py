import os.path
import pickle


class pantry(object):

    def __init__(self, filename):
        self.filename = filename

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        self._db = value

    @classmethod
    def open(cls, filename):
        p = cls(filename)
        p._open_pantry()
        return p

    @classmethod
    def store(cls, filename, obj):
        p = cls(filename)
        p._open_pantry()
        p._db = obj
        p.close()

    def close(self):
        self._close_pantry()

    def __enter__(self):
        self._open_pantry()
        return self.db

    def __exit__(self, *args, **kwargs):
        self._close_pantry()

    def _open_pantry(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                data = f.read()
                if data:
                    self._db = pickle.loads(data)
                else:
                    self._db = {}
        else:
            self._db = {}

    def _close_pantry(self):
        with open(self.filename, 'wb') as f:
            data = pickle.dumps(self._db)
            f.write(data)
