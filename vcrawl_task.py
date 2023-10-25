#!/usr/bin/env python
# -*- coding : UTF-8 -*-
from setting import *
from tools.config_parser import CrawlConfigParser
from tools.log import *
import traceback
import sys

class CrawlTask(object):
    def __init__(self, arguments):
        self.arguments = arguments

    def run(self):
        if "--conf" not in self.arguments:
            logger.error(f'submit cmd error ,can not find conf file!!{self.arguments}')
            raise Exception(f'submit cmd error ,can not find conf file!!')
        conf_file = self.arguments.get('--conf')
        task_id = self.arguments.get('--task_id')
        jobconf = CrawlConfigParser()
        workdir = os.getcwd()
        jobconf.read(os.path.join(workdir, conf_file))
        base_type = jobconf["base"]["type"]
        sub_type = jobconf["base"]["sub_type"]
        run_type = jobconf["others"]["run_type"]
        key = f"{base_type}_{sub_type}"
        logger.info(f"crawl type is {key},run_type is {run_type}")

        if key not in handler_list:
            logger.error(f"can not find the template {key}")
            return

        try:
            if 'once' == run_type:
                handler_list[key](jobconf).run(id=task_id)
            elif 'forever' == run_type:
                handler_list[key](jobconf).run_forever()
            else:
                logger.error(f"can not find the run_type {run_type}")
        except Exception as e:
            msg = traceback.format_exc()
            logger.error(f"{run_type} run error, error msg is {e} , msg{msg}")
            sys.exit()
