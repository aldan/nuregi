from setuptools import setup, find_packages
import pathlib

base_dir = pathlib.Path(__file__).parent.resolve()
long_description = (base_dir / 'README.md').read_text(encoding='utf-8')

setup(
    name='nuregi',
    version='0.1.0',
    description='A basic Python-based API client library for registrar.nu.edu.kz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aldan/nuregi',
    author='aldan',
    author_email='gitaldan@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Java',
        'Natural Language :: English',
    ],

    keywords='api library registrar.nu.edu.kz scraper',

    project_urls={
        'Source': 'https://github.com/aldan/nuregi',
        'Tracker': 'https://github.com/aldan/nuregi/issues',
    },

    packages=find_packages(),

    install_requires=[
        'requests',
        'numpy',
        'pandas',
        'tabula-py',
    ],

    python_requires='>=3.6',
)
