Data catalog to RDF library
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library for mapping a data catalog to rdf

The library contains helper classes for the following dcat classes:

* `Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_
* `Dataset <https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset>`_
* `Distribution <https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution>`_
* `Data Service <https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service>`_

Other relevant classes are also supported, such as:

* Contact (`vcard:Kind <https://www.w3.org/TR/2014/NOTE-vcard-rdf-20140522/#d4e1819>`_)

The library will map to `the Norwegian Application Profile <https://data.norge.no/specification/dcat-ap-no>`_ of `the DCAT standard <https://www.w3.org/TR/vocab-dcat-2/>`_.


Installation
------------

To install the datacatalogtordf package,
run this command in your terminal:

.. code-block:: console

   $ pip install datacatalogtordf


Usage
-----

This package can be used like this:

.. code-block:: python

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
  # Add concept to catalog:
  catalog.datasets.append(dataset)

  # get rdf representation in turtle (default)
  rdf = catalog.to_rdf(format="turtle")
  print(rdf.decode())

Will produce the following output:

.. code-block:: console

  @prefix dcat: <http://www.w3.org/ns/dcat#> .
  @prefix dct: <http://purl.org/dc/terms/> .

  <http://example.com/catalogs/1> a dcat:Catalog ;
      dct:publisher <https://example.com/publishers/1> ;
      dct:title "A dataset catalog"@en ;
      dcat:dataset <http://example.com/datasets/1> .

  <http://example.com/datasets/1> a dcat:Dataset ;
      dct:title "incomeAPI"@en,
          "inntekstAPI"@nb .
