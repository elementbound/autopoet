# Patch up import paths a bit
import os
from pathlib import Path

os.chdir(str(Path('.').absolute().parent))

import sys
import platform
import argparse

import autopoet.demos.wordstats as wordstats
import autopoet.demos.autosuggest as autosuggest

import autopoet.poetcrawler as poetcrawler

def main():
    # Fix up code-page
    if platform.system() == 'Windows':
        if sys.stdout.encoding != 'cp65001':
            print('Detected stdout encoding', sys.stdout.encoding)
            print('Setting it to cp65001')
            os.system('chcp 65001')
            sys.stdout.flush()

    demos = [wordstats, autosuggest]
    demo_names = [demo.__name__.split('.')[-1] for demo in demos]

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('demo', choices=demo_names, help='Target demo to run')
    parser.add_argument('-p', '--poet', choices=poetcrawler.available_poets, help='Set poet')

    args = sys.argv
    if args[0].startswith('py'):
        args = args[1:]
    args = parser.parse_args(args[1:])

    # Run the demo
    for demo in demos:
        if demo.__name__.endswith('.' + args.demo):
            demo.run(args)

main()
