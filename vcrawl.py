"""vcrawl

Usage:
  vcrawl.py crawl [--task_id=<v> --conf=<v>]
  vcrawl.py tg [--task_id=<v> --action=<v> ]


"""
from docopt import docopt
from vcrawl_task import CrawlTask
from task.tg_crawl_task import *

def run(argument):
    if argument.get("crawl"):
        CrawlTask(arguments).run()
    elif argument.get("tg"):
        TgCrawlTask(arguments).run()
    else:
        print(f'can not find run type = {argument}')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='vcrawl 1.0')
    run(arguments)
