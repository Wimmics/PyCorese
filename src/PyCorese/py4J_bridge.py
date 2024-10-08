"""Implementation of the Py4J bridge to Corese API in Java."""

import os
import subprocess
#import urllib.request
from time import sleep
from importlib import resources
from pathlib import Path
import logging

from py4j.java_gateway import JavaGateway

#from . import configure_logging
#configure_logging()

_CORESE_LIBRARY_PATH = Path(resources.files(__package__))\
                       .joinpath('jars/corese-library-python-4.5.0.jar')\
                       .resolve()
                       

class Py4JBridge:
    """
    Manage running Corese-Python Java library using Py4J.

    Parameters
    ----------
    corese_path : str, optional
        Path to the Corese-Python library. Default is None. If None, use the library 
        downloaded during package installation.

    """

    def __init__(self, corese_path: str|None =None):

        self.corese_path = corese_path or _CORESE_LIBRARY_PATH

        self.java_gateway = None

        if not os.path.exists(self.corese_path):
            raise FileNotFoundError(
                '\n'.join([f'CORESE library is not found at {self.corese_path}.',
                           f'Reinstall the {__package__} package.'])
            )

        # Register exit handler
        import atexit
        _ = atexit.register(self._exit_handler)
        
    def _exit_handler(self) -> None:
        if self.java_gateway is not None:
            self.java_gateway.shutdown()
        logging.info('CORESE is stopped')

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


		