import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="wagtail_responsive_images",
    version="0.0.1",
    author="Joshua Munn",
    author_email="jmunn@rkh.co.uk",
    description=("An app for generating responsive image sets with wagtail"),
    long_description=README,
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Framework :: Wagtail :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=["django", "wagtail", "lark", "pillow"],
    python_requires=">=3.4",
    extras_require={
        "testing": ["pytest"],
    },
)
