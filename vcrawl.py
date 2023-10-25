"""vcrawl

Usage:
  vcrawl.py crawl [--task_id=<v> --conf=<v>]
  vcrawl.py tg [--task_id=<v> --action=<v> ]


"""
from docopt import docopt
from tools.log import *
from vcrawl_task import CrawlTask


def run(argument):
    if argument.get("crawl"):
        CrawlTask(arguments).run()

    else:
        print(f'can not find run type = {argument}')

if __name__ == '__main__':
    arguments = docopt(__doc__, version='vcrawl 1.0')
    run(arguments)
