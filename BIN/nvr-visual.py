#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import re
import sys

from nvr.nvr import main

if __name__ == '__main__':
    a = ([re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])]
         + ['-s', '-c', 'doautocmd BufEnter']
         + sys.argv[1:])
    sys.exit(main(argv=a))
