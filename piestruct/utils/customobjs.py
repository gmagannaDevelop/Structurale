"""

  Author : Gustavo Magaña López

  This code is free for any use under the terms of
  the MIT license.

  This module should perhaps be split in
  semantically consistent scripts 

  io :
    * [ Path ]

  syntatic sugar :
    * [ ObjDict ]

"""


from pathlib import (
    Path as _Path_,
    PosixPath as _PosixPath_,
    WindowsPath as _WindowsPath_,
)
import os


class Path(_Path_):
    """
    Basically a wrapper for pathlib.Path,
    created to modify pathlib.Path.glob's behaviour :
      I don't like generators for practical purposes.

    I added a method lglob which returns a list instead
    of a generator.

    Thanks to this tread on code review :
      https://codereview.stackexchange.com/questions/162426/subclassing-pathlib-path
    """

    def __new__(cls, *args, **kvps):
        return super().__new__(
            WindowsPath if os.name == "nt" else PosixPath, *args, **kvps
        )

    def lglob(self, expr: str):
        """ Same as pathlib.Path.glob, but returns a list instead of a generator. """
        return list(super().glob(expr))

    def here(self, *args):
        """Precious utility method which yields a path object if the
        specified path exists, raising an exception otherwise."""
        _buffer = self.joinpath(*args)
        if _buffer.exists():
            return _buffer
        else:
            raise FileNotFoundError(f"File {_buffer.abs} does not exist")

    def dglob(self, expr: str):
        """Create a dictionary containing the files' names
        as keys and their Path object as value, matching a glob pattern."""
        return {entry.parts[-1]: entry for entry in super().glob(expr)}

    @property
    def abs(self):
        """ The absolute path to a file is a property, not a method. """
        return super().absolute().as_posix()


class WindowsPath(_WindowsPath_, Path):
    """ Helper for EZPath """

    pass


class PosixPath(_PosixPath_, Path):
    """ Helper for EZPath """

    pass


class ObjDict(dict):
    """
    Instantiate a dictionary that allows accesing values
    with object notation (as if they were attributes):

    ex:
        x.foo = 5
    instead of
        x['foo'] = 5

    The best part is that both ways work !

    Ideal for working with TOML files.

    Original code snippet found here :
    https://goodcode.io/articles/python-dict-object/
    """

    @property
    def lkeys(self):
        return super().keys()

    @property
    def lvalues(self):
        return super().values()

    @property
    def litems(self):
        return super().items()

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
