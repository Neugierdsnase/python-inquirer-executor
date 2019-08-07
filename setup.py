import setuptools
from inquirer_executor import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inquirer-executor",
    version=__version__,
    author="Konstantin Kovar",
    author_email="mail@vomkonstant.in",
    description="A package to tightly bind user choices to functionality. Based on python-inquirer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=['tests', 'examples']),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: ",
        "Libraries :: Application Frameworks",
    ],
    url='https://github.com/Neugierdsnase/python-inquirer-executor',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'blessings == 1.7',
        'readchar == 2.0.1',
        'python-editor==1.0.4',
    ],
    keywords='color terminal',
)
