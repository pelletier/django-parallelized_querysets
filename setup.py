from setuptools import setup
from parallelized_querysets import __version__


setup(
    name="django-parallelized_querysets",
    version=__version__,
    description="Spread Django QuerySets on multiple cores with low memory usage.",
    author="Thomas Pelletier",
    author_email="thomas@pelletier.im",
    license='MIT',
    url="https://github.com/pelletier/django-parallelized_querysets",
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Framework :: Django',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities'],
    packages=['parallelized_querysets'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools', 'django']
)
