from setuptools import setup, find_packages

setup(
    name='ova',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ova': ['*.json'],
    },
    install_requires=[
        'pytest==6.2.4',
        'requests==2.25.1',
        'rich==10.2.0',
        'discord.py==1.7.2'
    ],
)
