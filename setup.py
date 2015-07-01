from setuptools import setup, find_packages


setup(
    name = "Leadsheets",
    version = "0.1",
    packages = find_packages(),
    scripts = ['bin/leadsheets'],
    author = "Roman Dolgiy",
    author_email = "roman@btsolutions.co",
    description = "Demo project",
)