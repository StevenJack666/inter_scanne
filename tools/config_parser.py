from __future__ import absolute_import
import sys
if sys.version_info.major == 2:
    config_parser = __import__('ConfigParser')
else:
    config_parser = __import__('configparser')
class CrawlConfigParser(config_parser.RawConfigParser):
    def __init__(self,defaults=None):
        config_parser.ConfigParser.__init__(self,defaults=None)

    def optionxform(self, optionstr):
        return optionstr