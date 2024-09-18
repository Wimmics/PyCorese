#!/usr/bin/env python
# coding: utf-8
#
# JPype usage example
#
# Demonstrate loading and querying data with CoreseAPI
# connected through `JPype`.
#


import logging
import os
import sys
import time

from  PyCorese.api import CoreseAPI

#
data_path = os.path.abspath(os.path.join('data', 'beatles.rdf'))


# __main__
corese = CoreseAPI(java_bridge='jpype')

# start the JVM first to get java primitives
corese.loadCorese()

# now we can import java
import java
logging.info(f"java.lang.System.getProperty: {java.lang.System.getProperty('java.class.path')}")
corese_path = str(java.lang.System.getProperty('java.class.path'))

# add a shutdown hook to the java JVM
from jpype import JImplements, JOverride
@JImplements(java.lang.Runnable)
class MyShutdownHook:
    @JOverride
    def run(self):
        # perform any required shutdown activities
        logging.info("MyShutdownHook: here I am !")
        time.sleep(1)

java.lang.Runtime.getRuntime().addShutdownHook(java.lang.Thread(MyShutdownHook()))

def infoThread():
    logging.info(f"is_attached: {java.lang.Thread.isAttached()}")

# get some results now
graph = corese.loadRDF(data_path)
results = corese.query(graph)

infoThread()

print("="*80)
print(results)

#r0 = list(results)[0]

infoThread()

# Build/query a graph with `corese-core` classes exposed through `JPype`.

jpype_graph = corese.Graph()

# NameSpace
ex = "http://example.org/"

# Create and add statement: Edith Piaf is an Singer
edith_Piaf_IRI = jpype_graph.addResource(ex + "EdithPiaf")
rdf_Type_Property = jpype_graph.addProperty(corese.RDF.TYPE)
singer_IRI = jpype_graph.addResource(ex + "Singer")

jpype_graph.addEdge(edith_Piaf_IRI, rdf_Type_Property, singer_IRI)

query = "select ?s ?p ?o where {?s ?p ?o}"

exec = corese.QueryProcess.create(jpype_graph)

results = exec.query(query)

print("="*80)
print(results)

infoThread()

if False:
    # shutdown
    import jpype

    logging.info('Shutdown')
    jpype.shutdownJVM()

    infoThread()


    # restart
    jpype.startJVM(classpath=[corese_path])
    infoThread()
