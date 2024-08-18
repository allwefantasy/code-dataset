from setuptools import setup, find_packages

setup(
    name='code-dataset',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gitpython',
    ],
    entry_points={
        'console_scripts': [
            'code-dataset=code_dataset.cli:main',
        ],
    },
)