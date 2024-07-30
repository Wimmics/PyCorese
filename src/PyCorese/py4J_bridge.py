import os
import subprocess
import urllib.request
from time import sleep
import logging
from py4j.java_gateway import JavaGateway

#from . import configure_logging
#configure_logging()

#TODO: should we store the defaults somewhere else?
#leaving it like this until the distribution method is figured out
CORESE_LIBRARY_URL = 'http://files.inria.fr/corese/distrib/corese-library-python-4.5.0.jar' 
CORESE_LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'jars', 'corese-library-python-4.5.0.jar')


class Py4JBridge:
    """
    Manage running Corese-Python Java library using Py4J.
    
    :param corese_url: URL to download Corese library
    :param corese_path: Path to Corese library
    
    """

    def __init__(self, corese_url: str|None =None, corese_path: str|None =None):

        self.corese_url = corese_url or CORESE_LIBRARY_URL
        self.corese_path = corese_url or CORESE_LIBRARY_PATH

        self.java_gateway = None

        if not os.path.exists(self.corese_path):
            self._downloadCoresePython()
        else:
            logging.info('CORESE is already downloaded')

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)
	
    def __del__(self) -> None:
        """Destructor method for Py4JBridge."""
        self._exit_handler()
        
    def _exit_handler(self) -> None:
        if self.java_gateway is not None:
            self.java_gateway.shutdown()
        logging.info('CORESE is stopped')

    def _downloadCoresePython(self) -> None:
        """Download Corese-Python library."""  # noqa: D202

        try: 
            # create directory if it does not exist
            os.makedirs(os.path.dirname(self.corese_path), exist_ok=True)
            
            logging.info('Downloading CORESE from %s...', self.corese_url)
            urllib.request.urlretrieve(self.corese_url, self.corese_path)
            logging.info('CORESE is downloaded')
        
        except Exception as e:
            logging.error('CORESE failed to download: %s', str(e))
		
    def loadCorese(self) -> JavaGateway:
        """Load Corese-Python library in the context of Py4J."""
        # restart JVM if is already runningS
        if self.java_gateway is not None:
            self.java_gateway.shutdown()
            logging.info('Py4J: Stopped JVM with CORESE...')

        try:
            logging.info('Py4J: Loading CORESE...')
            subprocess.Popen(['java', '-jar', self.corese_path])
            sleep(0.1)

            self.java_gateway = JavaGateway()
            sleep(0.1)

            self.Graph = self.java_gateway.jvm.fr.inria.corese.core.Graph
            self.Load = self.java_gateway.jvm.fr.inria.corese.core.load.Load
            self.QueryProcess = self.java_gateway.jvm.fr.inria.corese.core.query.QueryProcess
            self.ResultFormat = self.java_gateway.jvm.fr.inria.corese.core.print.ResultFormat
            self.RDF = self.java_gateway.jvm.fr.inria.corese.core.logic.RDF
            
            logging.info('Py4J: CORESE is loaded')

        except Exception as e:
            logging.error('Py4J: CORESE failed to load: %s', str(e)) 

        return self.java_gateway


		