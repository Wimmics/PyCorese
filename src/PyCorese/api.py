"""The module provides the capability to launch corese-python jar."""

class CoreseAPI:
    """
    Python implementation of Corese API.

      :param bridge: Bridge name to use for Java integration ('py4j' or 'jpype'). Default is 'py4j'.
    """

    def __init__(self, java_bridge: str = 'py4j'):
        
        if java_bridge.lower() not in ['py4j', 'jpype']:
            raise ValueError('Invalid java bridge. Only "py4j" and "jpype" are supported.')

        self.java_bridge = java_bridge.lower()
        self.java_gateway = None

        self.Graph = None
        self.QueryProcess = None
        self.ResultFormat = None
        self.Load = None

	
    def __del__(self) -> None:
        if self.java_gateway:
            del self.java_gateway
		
    def loadCorese(self) -> None:

        if self.java_bridge == 'py4j':
           
            from .py4J_bridge import Py4JBridge

            java_bridge = Py4JBridge()
            self.java_gateway = java_bridge.loadCorese()


            self.Graph = java_bridge.Graph
            self.Load = java_bridge.Load
            self.QueryProcess = java_bridge.QueryProcess
            self.ResultFormat = java_bridge.ResultFormat
            self.RDF = java_bridge.RDF
            
        else:

            from .jpype_bridge import JPypeBridge

            java_bridge = JPypeBridge()
            self.java_gateway = java_bridge.loadCorese()


            self.Graph = java_bridge.Graph
            self.Load = java_bridge.Load
            self.QueryProcess = java_bridge.QueryProcess
            self.ResultFormat = java_bridge.ResultFormat
            self.RDF = java_bridge.RDF



    def loadRDF(self, rdf_file: str, graph=None) :
        if not self.java_gateway:
            self.loadCorese()
        
        if not graph:
            graph = self.Graph()

        ld = self.Load().create(graph)
        ld.parse(rdf_file)

        return graph

    def query(self, graph, query: str ='SELECT * WHERE {?s ?p ?o} LIMIT 5' , prefixes=''):
        
        if not self.java_gateway:
            self.loadCorese()

        exec = self.QueryProcess.create(graph)
        map = exec.query('\n'.join([prefixes, query]) )

        resultFormat = self.ResultFormat.create(map, self.ResultFormat.SPARQL_RESULTS_CSV)

        return resultFormat

#cr = CoreseAPI(java_bridge='jpype')
#cr.launchCorese()
#del cr

