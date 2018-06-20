import sys
import logging


CONFIGURATION = {
    "debug": True,
    "TOKEN": "",
    "HOST": "",
    "THRESHOLD": 0.35

}


def get(key, default=None):
    if key in CONFIGURATION:
        return CONFIGURATION[key]

    if default:
        return default

    logging.fatal("No setting for %s found in config.py" % key)
    sys.exit(1)
