from setuptools import setup, find_packages

setup(
    name='recruitment tasks',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='Konrad Bonder',
    author_email='konrad.bonder@gmail.com',
    description='solved recruitment tasks',
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
)
