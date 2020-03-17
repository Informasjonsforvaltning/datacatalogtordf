![Tests](https://github.com/Informasjonsforvaltning/datacatalogtordf/workflows/Tests/badge.svg)
# datacatalogtordf

A small Python library for mapping a data catalog to rdf

The library contains helper classes for the following dcat classes:
 - [Catalog](https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog)
 - [Dataset](https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset)
 - [Distribution](https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution)
 - [Data Service](https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service)

 Other relevant classe are also supported, such as:
 - Contact [vcard:Kind](https://www.w3.org/TR/2014/NOTE-vcard-rdf-20140522/#d4e1819)

 The library will map to [the Norwegian Application Profile](https://doc.difi.no/dcat-ap-no/).

## Usage
### Install
```
% pip install -i datacatalogtordf
```
### Getting started
```
from datacatalogtordf.catalog import Catalog, Dataset

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
# Add concept to catalog:
catalog.datasets.append(dataset)

# get rdf representation in turtle (default)
rdf = catalog.to_rdf()
print(rdf.decode())
```
## Development
### Requirements
- python3
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

### Install
```
% git clone https://github.com/Informasjonsforvaltning/datacatalogtordf.git
% cd datacatalogtordf
% pyenv install 3.8.2
% pyenv install 3.7.6
% pyenv local 3.8.2 3.7.6
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
nox -rs tests -- --pdb
```
You can set breakpoints directly in code by using the function `breakpoint()`.
