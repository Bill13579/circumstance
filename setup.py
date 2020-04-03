import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cir",
    version="0.0.1",
    author="Bill K.",
    author_email="bluesky42624@gmail.com",
    description="Manage nested file path in Python easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bill13579/circumstance",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)