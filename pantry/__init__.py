import os.path
import pickle
import inspect
import linecache
import ast


class pantry(object):

    def __init__(self, filename, frame_magic=False):
        self.filename = filename
        self.frame_magic = frame_magic

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

    def _capture_unbound_var_name(self, frame):
        # collect basic information from frame
        filename = frame.f_back.f_code.co_filename
        lineno = frame.f_back.f_lineno
        # Assuming the single line returned is valid, remove leading
        # indent and append pass to allow this be parsed.
        tree = ast.parse(linecache.getline(filename, lineno).strip() + 'pass')
        # This is the name that the return value of __enter__ will bound
        # to
        self._bound_to = tree.body[0].items[0].optional_vars.id

    def __enter__(self):
        if self.frame_magic:
            frame = inspect.currentframe()
            self._capture_unbound_var_name(frame)
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
        if self.frame_magic:
            frame = inspect.currentframe()
            # grab the bounded value from the target frame.
            # structured as: current, __exit__, target
            self._db = frame.f_back.f_back.f_locals[self._bound_to]

        with open(self.filename, 'wb') as f:
            data = pickle.dumps(self._db)
            f.write(data)
