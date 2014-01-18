from setuptools import setup, find_packages

setup(
    name = 'tweet-music',
    version = '0.0.2',
    description = "",
    long_description = "",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords = 'Art, Music, Midi, Twitter',
    author = 'Brian Abelson',
    author_email = 'brianabelson@gmail.com',
    url = 'http://github.com/csvsoundsystem/tweet-music',
    license = 'MIT',
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages = [],
    include_package_data = False,
    zip_safe = False,
    install_requires = [
        "Cython==0.19.2",
         "python-rtmidi==0.4.3b1",
         "tweepy==2.1",
         "wsgiref==0.1.2"
    ],
    tests_require = []
)