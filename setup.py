import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datacatalogtordf",
    version="1.0.0.dev01",
    author="Stig B. Dørmænen",
    author_email="sbd@digdir.no",
    description=(
                 "A small Python library for mapping a data catalog"
                 " to the dcat-ap-no specification"
                 ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Informasjonsforvaltning/datacatalogtordf",
    packages=setuptools.find_packages(),
    install_requires=[
        'rdflib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
