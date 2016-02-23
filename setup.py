import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pymonero",
    version = "0.0.1",
    description = ("A Monero daemon RPC connection tool in python."),
    url = "https://github.com/Monero-Monitor/pymonero",
    license = "BSD 3-Clause",
    author = "Mike C",
    keywords = "monero",
    packages=['pymonero'],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=["requires"],
    zip_safe=False
)