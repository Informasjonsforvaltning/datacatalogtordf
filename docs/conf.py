"""Sphinx configuration."""
project = "datacatalogtordf"
author = "Stig B. Dørmænen"
copyright = f"2020, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]
intersphinx_mapping = {
    "concepttordf": ("https://concepttordf.readthedocs.io/en/latest", None),
    "python": ("https://docs.python.org/3", None),
}
