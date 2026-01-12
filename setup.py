from setuptools import setup, find_packages

setup(
    name='lightoracle',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'keyring',
        'oracledb==2.2.1',
        'python-dotenv'
    ],
    author='Isaac Kerson',
    author_email='ikerson@gsu.edu',
    description='A lightweight Oracle database connection handler.',
    keywords='oracle database connection pandas',
    url='https://github.com/GSU-Analytics/lightoracle.git', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
