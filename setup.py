from setuptools import setup, find_packages
import os

# 读取 README.md 文件内容作为 long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt 文件内容
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='code-dataset',
    version='0.1.1',
    author='WilliamZhu',
    author_email='allwefantsy@gmail.com',
    description='A tool for managing code datasets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code_dataset",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'code-dataset=code_dataset.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)