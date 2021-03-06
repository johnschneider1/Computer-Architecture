#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# if len(sys.argv) != 2:
#     print("Usage: file.py filename", file=sys.stderr)
#     sys.exit(1)

cpu = CPU(sys.argv[1])


cpu.load()
cpu.run()
