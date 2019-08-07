import setuptools
from inquirer_executor import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inquirer_executor",
    version=__version__,
    author="Konstantin Kovar",
    author_email="mail@vomkonstant.in",
    description="A package to tightly bind user choices to functionality. Based on python-inquirer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Neugierdsnase/python-inquirer-executor",
    packages=setuptools.find_packages(include=["inquirer_executor"]),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    install_requires=["inquirer == 2.6.3"],
    keywords="color terminal",
)
