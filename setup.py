from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]


setup(
    name='mpim-icelab',
    version='0.1.0',
    author='Markus Ritschel',
    author_email='git@markusritschel.de',
    description='A collection of routines for various tasks related to the sea-ice laboratory of the Max-Planck-Institute for Meteorology in Hamburg',
    long_description=readme,
    license="MIT license",
    keywords=(
        "Python, mpim-icelab"
    ),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    url='https://github.com/markusritschel/mpim-icelab',
    packages=find_packages(include=['mpim-icelab', 'mpim-icelab.*']),
    install_requires=setup_requirements,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
