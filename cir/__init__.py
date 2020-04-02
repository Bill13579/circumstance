import os
import threading
import inspect

class cir:
    _active_group = threading.local()
    
    def __init__(self, p):
        super().__init__()
        self.__p = p
    
    @property
    def path(self):
        return self.__p
    
    def __enter__(self):
        if not hasattr(cir._active_group, 'current'):
            cir._active_group.current = []
        stack = cir._active_group.current
        cir._active_group.current.append(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        last = cir._active_group.current.pop()
        assert last == self, "Context managers being exited out of order"
    
    def __call__(self, sub="", *more):
        return os.path.normpath(os.path.join(*[i.path for i in cir._active_group.current], sub, *more))

    @classmethod
    def cd(cls, where, *more):
        return cls(os.path.join(where, *more))

    @classmethod
    def working(cls):
        return cls(os.getcwd())

    @classmethod
    def me(cls):
        return cls(os.path.abspath(os.path.dirname(inspect.stack()[1].filename)))

cd = cir.cd
working = cir.working
me = cir.me