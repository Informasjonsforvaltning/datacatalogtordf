# datacatalogtordf

![Tests](https://github.com/Informasjonsforvaltning/datacatalogtordf/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/datacatalogtordf/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/datacatalogtordf)
[![PyPI](https://img.shields.io/pypi/v/datacatalogtordf.svg)](https://pypi.org/project/datacatalogtordf/)
[![Read the Docs](https://readthedocs.org/projects/datacatalogtordf/badge/)](https://datacatalogtordf.readthedocs.io/)

A small Python library for mapping a data catalog to rdf

The library contains helper classes for the following dcat classes:

- [Catalog](https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog)
- [Dataset](https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset)
- [Distribution](https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution)
- [Data Service](https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service)

 Other relevant classes are also supported, such as:

- Contact [vcard:Kind](https://www.w3.org/TR/2014/NOTE-vcard-rdf-20140522/#d4e1819)

 The library will map to [the Norwegian Application Profile](https://data.norge.no/specification/dcat-ap-no) of [the DCAT standard](https://www.w3.org/TR/vocab-dcat-2/).

## Usage

### Install

```Shell
% pip install datacatalogtordf
```

### Getting started

```Python
from datacatalogtordf import Catalog, Dataset

# Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A dataset catalog"}
catalog.publisher = "https://example.com/publishers/1"

# Create a dataset:
dataset = Dataset()
dataset.identifier = "http://example.com/datasets/1"
dataset.title = {"nb": "inntektsAPI", "en": "incomeAPI"}
#
# Add dataset to catalog:
catalog.datasets.append(dataset)

# get rdf representation in turtle (default)
rdf = catalog.to_rdf(format="turtle")
print(rdf.decode())
```

Will produce the following output:

```Shell
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://example.com/catalogs/1> a dcat:Catalog ;
    dct:publisher <https://example.com/publishers/1> ;
    dct:title "A dataset catalog"@en ;
    dcat:dataset <http://example.com/datasets/1> .

<http://example.com/datasets/1> a dcat:Dataset ;
    dct:title "incomeAPI"@en,
        "inntekstAPI"@nb .
```

## Development

### Requirements

You need [uv](https://docs.astral.sh/uv/) to manage dependencies and run the application.

Install it with:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or follow the instructions on the [uv website](https://docs.astral.sh/uv/getting-started/installation/).

### Install developer tools

```Shell
% git clone https://github.com/Informasjonsforvaltning/datacatalogtordf.git
% cd datacatalogtordf
% uv sync
```


### Run all sessions

```Shell
% uv run poe release
```

### Run all tests with coverage reporting

```Shell
% uv run poe tests
```

### Debugging

You can set breakpoints directly in code by using the function `breakpoint()`.

Run the tests with the `--pdb` flag to enter the debugger when a test fails:

```Shell
% uv run --python 3.13 pytest --capture=no --pdb
```
