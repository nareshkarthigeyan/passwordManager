from setuptools import setup, find_packages

setup(
    name='passman',
    version='0.0.1',
    description='A password manager application',
    author='Naresh Karthigeyan',
    author_email='nareskarthigeyan.2005@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tabulate',
        'rsa',
    ],
    entry_points={
        'console_scripts': [
            'passman = passman.main:main',
        ],
    },
)
