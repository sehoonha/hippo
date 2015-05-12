#!/usr/bin/env python

import pydart
import logging
from simulation import Simulation
from window import Window
import utils
import sys

# from logging_tree import printout  # pip install logging_tree
# printout()
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.handlers = []

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logfmt = '[%(levelname)s][%(asctime)s][%(module)s:%(lineno)d] %(message)s'
formatter = logging.Formatter(logfmt)
ch.setFormatter(formatter)
root.addHandler(ch)

# Get a logger for this file
logger = logging.getLogger(__name__)
logger.info('Green stair project')

# Register jsonpickle numpy handler
utils.jsonpickle_numpy.register_handlers()

sim = Simulation()
# Run the application
pydart.qtgui.run(title=sim.title(), simulation=sim, cls=Window)
