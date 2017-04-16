# Patch up import paths a bit
import os
from pathlib import Path

os.chdir(str(Path('.').absolute().parent))

import sys
import argparse

import autopoet.demos.wordstats as wordstats

def main():
    demos = [wordstats]
    demo_names = [demo.__name__.split('.')[-1] for demo in demos]

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('demo', choices=demo_names, help='Target demo to run')

    args = sys.argv
    if args[0].startswith('py'):
        args = args[1:]
    args = parser.parse_args(args[1:])

    # Run the demo
    for demo in demos:
        if demo.__name__.endswith('.' + args.demo):
            demo.run()

main()
