# What is this?

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

# Installation

Installation is as simple as `pip install cir`

#### Requirements

- Python >= 3.5

# Documentation

[Documentation](https://bill13579.github.io/circumstance/cir/)