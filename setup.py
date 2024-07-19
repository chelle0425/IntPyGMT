from setuptools import setup

setup(
    name='IntPyGMT',
    version='0.1.0',
    description='An interactive map tool for pyGMT',
    url='https://github.com/chelle0425/interactive_pygmt',
    author='Rochelle Pun',
    author_email='rochelle.pun@gmail.com',
    packages=['IntPyGMT'],
    package_dir = {'IntPyGMT':'python'},
    install_requires = [
        'numpy<2.0',
        'matplotlib',
        'ipympl',
        'basemap',
        'pillow']
)