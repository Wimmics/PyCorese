#!/usr/bin/env python
# coding: utf-8

import os
data_path = os.path.abspath(os.path.join('data', 'beatles.rdf'))


import importlib.util

package_name = 'PyCorese'
useLocal = True # used for development

if useLocal:
    import sys
    sys.path.insert(0, '..\\src')

if importlib.util.find_spec(package_name):
    print(f"'{package_name}' is installed")
else:
    print(f"'{package_name}' is not installed")
    get_ipython().system('pip install install git+https://github.com/annabobasheva/PyCorese.git')


# ## Py4J
#
# Demonstrate loading and querying data with CoreseAPI connected through `Py4J`.

from  PyCorese.api import CoreseAPI

if 'corese' in locals():
    del corese

corese = CoreseAPI(java_bridge='Py4J')

corese.loadCorese()
graph = corese.loadRDF(data_path)
results = corese.query(graph)

print(results)


# Build/query a graph with `corese-core` classes exposed through `Py4J`.


py4j_graph = corese.Graph()

# NameSpace
ex = "http://example.org/"

# Create and add statement: Edith Piaf is an Singer
edith_Piaf_IRI = py4j_graph.addResource(ex + "EdithPiaf")
rdf_Type_Property = py4j_graph.addProperty(corese.RDF.TYPE)
singer_IRI = py4j_graph.addResource(ex + "Singer")

py4j_graph.addEdge(edith_Piaf_IRI, rdf_Type_Property, singer_IRI)

query = "select ?s ?p ?o where {?s ?p ?o}"

exec = corese.QueryProcess.create(py4j_graph)

results = exec.query(query)

print(results)
