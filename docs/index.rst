Data catalog to RDF library
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

Installation
------------

To install the datacatalogtordf package,
run this command in your terminal:

.. code-block:: console

   $ pip install datacatalogtordf


Usage
-----

This package can be used like this:

.. code-block::

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
