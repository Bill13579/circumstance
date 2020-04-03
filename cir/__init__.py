"""
# What is Circumstance?

In Python, when you're trying to deal with multiple nested directories, there's one problem that can make your code harder to understand: The Concat Hell.

For example, if I have my config files and folders setup like this:
```
app
├── app.log
├── config.json
├── icons
│   ├── add.ico
│   ├── divide.ico
│   ├── multiply.ico
│   └── subtract.ico
└── logo
    ├── 128.ico
    ├── 32.ico
    └── 64.ico
```

To load all of them using **Just Python**:
```python
### Just Python
def load_resources():
    ROOT = os.path.abspath(os.path.dirname(__file__))
    config = load_config(ROOT + "/config.json")
    logos = {
        32: load_image(ROOT + "/logo/32.ico"),
        64: load_image(ROOT + "/logo/64.ico"),
        128: load_image(ROOT + "/logo/128.ico")
    }
    add_icon = load_icon(ROOT + "/icons/add.ico")
    divide_icon = load_icon(ROOT + "/icons/divide.ico")
    multiply_icon = load_icon(ROOT + "/icons/multiply.ico")
    subtract_icon = load_icon(ROOT + "/icons/subtract.ico")
    logger.setPath(ROOT + "/app.log")
```

As you can see, there's ***a lot*** of string concatenations! Not only that, if we forget what `ROOT` represents, we might get buggy code! 

To load all of them using **Circumstance**:
```python
### Using Circumstance
def load_resources():
    with cir.me() as root_:
        config = load_config(root_("config.json"))
        with root_.cd("logo") as logos_:
            logos = {
                32: load_image(logos_("32.ico")),
                64: load_image(logos_("64.ico")),
                128: load_image(logos_("128.ico"))
            }
        with root_.cd("icons") as icons_:
            add_icon = load_icon(icons_("add.ico"))
            divide_icon = load_icon(icons_("divide.ico"))
            multiply_icon = load_icon(icons_("multiply.ico"))
            subtract_icon = load_icon(icons_("subtract.ico"))
        logger.setPath(root_("app.log"))
```

We have eliminated any string concatenations.
"""

import os
import threading
import inspect

class cir:
    """
    Object representing a folder context
    
    Typically instantiated indirectly using `cir.cd`, `cir.working`, or `cir.me`.
    Typically used in conjunction with "with"

    Example:
    ```python
    # In practice, it is recommended to use "cir.cd", "cir.working", or "cir.me" instead of this
    with cir.cir("path/") as resolve:
      print(resolve("file"))
    ```
    """
    _active_group = threading.local()
    
    def __init__(self, path):
        """Initializes a new folder context"""
        super().__init__()
        self.__p = path
    
    @property
    def path(self):
        """Path represented by the `cir` instance"""
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
        """
        (Alias for cir.resolve)
        Resolve the provided sub-path `sub` plus any additional paths `*more`, using the current context
        """
        return cir.resolve(sub, *more)

    @classmethod
    def resolve(cls, sub="", *more):
        """
        Resolve the provided sub-path `sub` plus any additional paths `*more`, using the current context
        """
        return os.path.normpath(os.path.join(*[i.path for i in cls._active_group.current], sub, *more))

    @classmethod
    def cd(cls, where, *more):
        """
        Go into the specified directory `where` plus any additional paths `*more`, and return the sub-`cir.cir`

        Example:
        ```python
        # Used independently
        with cir.cd("/home") as home_:
          print(home_("tom"))  # Output: /home/tom
        
        # Used in conjunction with "cir.me"
        with cir.me() as here_:
          with cir.cd("resources") as res_:
            print(res_("example.png"))  # Output: <folder where the calling file resides>/resources/example.png
        ```
        """
        return cls(os.path.join(where, *more))

    @classmethod
    def working(cls):
        """
        Go into the current working directory and return a new context of type `cir.cir`

        Example:
        ```python
        with cir.working() as working_:
          print(working_("example.png"))  # Output: <working directory>/example.png
        ```
        """
        return cls(os.getcwd())

    @classmethod
    def me(cls):
        """
        Go into the parent directory of the calling function's file and return a new context of type `cir.cir`
        
        Example:
        ```python
        with cir.me() as here_:
          print(here_("example.png"))  # Output: <folder where the calling file resides>/example.png
        ```
        """
        return cls(os.path.abspath(os.path.dirname(inspect.stack()[1].filename)))

cd = cir.cd
working = cir.working
me = cir.me