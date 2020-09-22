import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='dataapi-client',
    version='0.0.1',
    author='Jacques Nel',
    author_email='jmnel92@gmail.com',
    description='Research data server API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jmnel/dataapi-client',
    install_requires=[
        'requests>=2',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
