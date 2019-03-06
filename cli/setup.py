from setuptools import setup, find_packages

def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()

setup(
    name="quicklinks",
    version='0.1.1',
    author='Shubham Naik',
    author_email='shub@shub.club',
    description='Quickly navigate to websites based on shorthands you provide',
    long_description=read_file('../README.md'),
    url='https://github.com/4shub/quicklinks/',
    py_modules=['quicklinks'],
    zip_safe=False,
    license='MIT',
    entry_points= {
        "console_scripts": [
            "ql = quicklinks:main",
        ]
    }
)