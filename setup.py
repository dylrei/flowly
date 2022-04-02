"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='flowly',
    version='0.1',
    description='A platform for authoring and executing workflow content',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dylrei/flowly',
    author='Dylan Reinhardt',
    author_email='dylan@dylrei.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    project_urls={
        'Bug Reports': 'https://github.com/dylrei/flowly/issues',
        'Source': 'https://github.com/dylrei/flowly/',
    },
)