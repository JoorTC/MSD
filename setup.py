import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.3'
PACKAGE_NAME = 'missedSampleLib'
AUTHOR = 'Jordi Tortosa Carreres'
AUTHOR_EMAIL = 'tortosacarreresjordi@gmail.com'
URL = "https://github.com/JoorTC/MSD"

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'missedSampleLib'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

# INSTALL_REQUIRES = []

setup(
    name="missedSampleLib",
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'missedSampleLib', 'misidentified samples'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)