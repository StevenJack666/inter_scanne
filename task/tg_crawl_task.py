#!/usr/bin/env python
# -*- coding : UTF-8 -*-
import sys
import traceback
from tg_spiders.handler.tg_strategy import *
from tools.config_parser import CrawlConfigParser
from tools.log import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))

class TgCrawlTask(object):
    def __init__(self, arguments):
        self.root_path = get_root_path()
        self.arguments = arguments
        self.session_file = self.root_path + 'conf/tg_config.json'
        self.app_conf = self.root_path + 'conf/application.conf'

    def run(self):
        action = self.arguments.get('--action')
        task_id = self.arguments.get('--task_id')
        logger.info(f"tg tg type is {action},task_id is {task_id}")
        if action not in tg_handler_list:
            logger.error(f"can not find the template {action}")
            return
        try:
            tg_handler_list[action](self.session_file, self.app_conf).run(id=task_id)
            sys.exit()
        except Exception as e:
            msg = traceback.format_exc()
            logger.error(f"{action} run error, error msg is {e}, msg_trackback is {msg}")
            sys.exit()


