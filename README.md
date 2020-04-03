# What is this?

In Python, when you're trying to deal with multiple nested directories, there's one problem that makes your code hard to understand: The Concat Hell.

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
    with cir.me() as root:
        config = load_config(root("config.json"))
        with root.cd("logo") as logo_path:
            logos = {
                32: load_image(logo_path("32.ico")),
                64: load_image(logo_path("64.ico")),
                128: load_image(logo_path("128.ico"))
            }
        with root.cd("icons") as icon_path:
            add_icon = load_icon(icon_path("add.ico"))
            divide_icon = load_icon(icon_path("divide.ico"))
            multiply_icon = load_icon(icon_path("multiply.ico"))
            subtract_icon = load_icon(icon_path("subtract.ico"))
        logger.setPath(root("app.log"))
```

We have eliminated any string concatenations.

# API

## cir.**cir(path)**
```python
  Object representing a folder context

  Typically used in conjunction with "with"

  Example:
    with cir.cir("path/path/path") as resolve:
      print(resolve("file"))
```

### cir.cir.**path**
```python
Path represented by a "cir.cir"
```

### cir.cir.**\_\_enter\_\_**
### cir.cir.**\_\_exit\_\_**
```python
Context manager methods
```

### cir.cir.**\_\_call\_\_(self, sub="", \*more)**
```python
Alias for "cir.cir.resolve"
```


### cir.cir.**resolve(cls, sub="", \*more)**
```python
CLASSMETHOD!!!
Resolve the provided sub-path plus any additional paths with the current context
```

### cir.**cd(cls, where, \*more)**
### cir.cir.**cd(cls, where, \*more)**
```python
CLASSMETHOD!!
Go into the specified directory "where" plus any additional paths and return the sub-"cir.cir"
```

### cir.**working(cls)**
### cir.cir.**working(cls)**
```python
CLASSMETHOD!!
Go into the current working directory and return the "cir.cir"(basically the context)
```

### cir.**me(cls)**
### cir.cir.**me(cls)**
```python
CLASSMETHOD!!
Go into the parent directory of the calling function's module file and return the "cir.cir"(basically the context)
```