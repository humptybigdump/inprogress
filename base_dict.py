import numpy as np
import copy

from sortedcontainers import SortedDict
from numpy import ndarray


class BaseDict(SortedDict):

    default = None

    def __getitem__(self, key):
        if isinstance(key, (list, tuple)):
            # return all matching keys, raise KeyError if key doesn't exist
            return [self[k] for k in key]
        elif isinstance(key, ndarray):
            return [self[k] for k in key.tolist()]
        elif isinstance(key, slice):
            slice_list = list(range(*key.indices(max(self.keys()) + 1)))
            return [self[k] for k in slice_list]
        else:
            return super(BaseDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, (list, tuple, slice)):
            self.update(SortedDict(zip(key, value)))
        elif isinstance(key, ndarray):
            self.update(SortedDict(zip(key.tolist(), value.tolist())))
        else:
            super(BaseDict, self).__setitem__(key, value)

    def __deepcopy__(self, memodict={}):
        items = copy.deepcopy(list(self.items()))
        new = self.__class__(items)
        return new

    @property
    def list(self):
        return self.values()

    @property
    def array(self):
        # TODO: This will fail when nodes have different length
        return np.asarray(self.list)
