from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

from collections.abc import MutableMapping
from collections.abc import Mapping

from numpy import ndarray
from .base_dict import BaseDict


class History(BaseDict):

    def __init__(self, dictionary=None):
        """Defines and manages a history sorted dictionary."""
        if dictionary:
            super(History, self).__init__(dictionary)
        else:
            super(History, self).__init__()

    def __setitem__(self, key, value):
        if isinstance(key, float):
            if isinstance(value, (Mapping, MutableMapping)):
                # assert 'bc_u' in value.keys()
                # assert 'bc_f' in value.keys()
                assert "Ui" in value.keys()
                super(History, self).__setitem__(key, value)
            elif value is None:
                super(History, self).__setitem__(key, value)
            else:
                raise ValueError("History values must be None or dictionary-like.")
        else:
            raise ValueError("History keys must be control values.")

    def __getitem__(self, key):
        if isinstance(key, (list, tuple)):
            # return all matching keys, raise KeyError if key doesn't exist
            return [self[k] for k in key]
        elif isinstance(key, ndarray):
            return [self[k] for k in key.tolist()]
        elif isinstance(key, slice):
            slice_list = list(range(*key.indices(max(self.keys()))))
            return [self[k] for k in slice_list]
        elif isinstance(key, int):
            return self[self.keys()[key]]
        else:
            return super(BaseDict, self).__getitem__(key)
