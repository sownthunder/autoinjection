<<<<<<< HEAD
#!/usr/bin/env python

import logging
import optparse
import sys

sys.dont_write_bytecode = True

__import__("lib.utils.versioncheck")  # this has to be the first non-standard import

from sqlmap import modulePath
from lib.core.common import setPaths
from lib.core.data import logger
from lib.core.settings import RESTAPI_DEFAULT_ADAPTER
from lib.core.settings import RESTAPI_DEFAULT_ADDRESS
from lib.core.settings import RESTAPI_DEFAULT_PORT
from lib.utils.api import client
from lib.utils.api import server

def main():
    """
    REST-JSON API main function
    """

    # Set default logging level to debug
    logger.setLevel(logging.DEBUG)

    # Initialize paths
    setPaths(modulePath())

    server(RESTAPI_DEFAULT_ADDRESS, RESTAPI_DEFAULT_PORT, adapter=RESTAPI_DEFAULT_ADAPTER)

if __name__ == "__main__":
    main()
=======

>>>>>>> origin/master
