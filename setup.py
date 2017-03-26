from setuptools import setup, find_packages

setup(
    name='lazydir',
    version=0.1,
    author='Alex Peitsinis',
    py_modules=['lazydir'],
    entry_points={
        'console_scripts': [
            'lazydir = lazydir:main'
        ]
    },
    zip_safe=False
)
