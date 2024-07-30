import os
import urllib.request
import logging
import jpype
import jpype.imports
from jpype.types import *  

#from . import configure_logging
#configure_logging()


#TODO: should we store the defaults somewhere else?
#leaving it like this until the distribution method is figured out

CORESE_LIBRARY_URL = 'https://repo1.maven.org/maven2/fr/inria/corese/corese-core/4.5.0/corese-core-4.5.0-jar-with-dependencies.jar' 
CORESE_LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'jars', 'corese-core-4.5.0-jar-with-dependencies.jar')


class JPypeBridge:
    """
    Python implementation of Corese API.
    
    :param corese_url: URL to download Corese library
    :param corese_path: Path to Corese library
    
    """

    def __init__(self, corese_url=None, corese_path=None):

        self.corese_url = corese_url or CORESE_LIBRARY_URL
        self.corese_path = corese_url or CORESE_LIBRARY_PATH

        if not os.path.exists(self.corese_path):
            self._downloadCoreseCore()
        else:
            logging.info('JPype: Corese-core is already downloaded')

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)
	
    def __del__(self):
        self._exit_handler()
        
    def _exit_handler(self):
        jpype.shutdownJVM()
        logging.info('CORESE is stopped')


    def _downloadCoreseCore(self):
        """Download Corese-core library with dependencies."""
        try: 
            # create directory if it does not exist
            os.makedirs(os.path.dirname(self.corese_path), exist_ok=True)
            
            logging.info('Downloading CORESE from %s...', self.corese_url)
            urllib.request.urlretrieve(self.corese_url, self.corese_path)
            logging.info('CORESE is downloaded')
        
        except Exception as e:
            logging.error('CORESE failed to download: %s', str(e))

			
    def loadCorese(self) -> jpype:
        """Load Corese library into context of JPype."""  
        # Because of lack of JVM support, you cannot shutdown the JVM and then restart it.
        # Nor can you start more than one copy of the JVM.
        # https://jpype.readthedocs.io/en/latest/install.html#known-bugs-limitations

        # catch the exception if corese cannot start
        try:

            # check if JVM is already running
            if jpype.isJVMStarted():
                logging.info('JPype: JVM is already running')
            else:
                logging.info('JPype: Loading CORESE...')
                jpype.startJVM(classpath=[self.corese_path])


            # Import of class
            from fr.inria.corese.core import Graph
            from fr.inria.corese.core.load import Load
            from fr.inria.corese.core.logic import RDF
            from fr.inria.corese.core.print import ResultFormat
            from fr.inria.corese.core.query import QueryProcess

            self.Graph = Graph
            self.Load = Load
            self.QueryProcess = QueryProcess
            self.ResultFormat = ResultFormat
            self.RDF = RDF

            logging.info('JPype: CORESE is loaded')


        except Exception as e:
            logging.error('JPype: CORESE failed to load: %s', str(e)) 
     

        return jpype
    

		