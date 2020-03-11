from rdflib import Namespace

DCT = Namespace('http://purl.org/dc/terms/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')


class Distribution():
    """
    A class representing dcat:Distribution
    """

    def __init__(self):
        self._type = DCAT.Distribution
