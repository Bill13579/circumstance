import cir

with cir.me() as root:
    with cir.cd("cir") as source_dir:
        print(source_dir("__pycache__", "cache.py"))