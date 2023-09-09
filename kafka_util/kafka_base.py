#!/usr/bin/env python
# coding=utf-8

from tools.log import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))

class KafkaBase(object):
    session = None



    def __init__(self, kafkaconf):
        self.bootstrap_servers = kafkaconf["kafka"]["address"]
