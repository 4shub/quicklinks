from setuptools import setup, find_packages

def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()


setup(
    name="quicklinks",
    version='0.1.3',
    author='Shubham Naik',
    author_email='shub@shub.club',
    description='Quickly navigate to websites based on shorthands you provide',
    long_description=read_file('../README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/4shub/quicklinks/',
    py_modules=['quicklinks'],
    packages=['api'],
    install_requires=read_file('./requirements.txt'),
    zip_safe=False,
    license='MIT',
    entry_points= {
        "console_scripts": [
            "ql = quicklinks:main",
        ]
    },
    setup_requires=[
        'setuptools>=41.0.1',
    ]
)