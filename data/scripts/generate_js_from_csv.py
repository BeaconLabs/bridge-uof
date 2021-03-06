"""Generates a javascript file that contains criminal code data."""

import sys


def process(infile, outfile, varname):
    """Read data from infile and generate js at outfile."""
    outlines = [
        "// This file was automatically generated by a rule in the Makefile",
        "window.%s = [" % varname.upper(),
    ]
    for line in open(infile).read().splitlines():
        outlines.append('  "%s",' % line.replace('"', '\\"'))
    outlines[-1] = outlines[-1][:-1]  # Remove trailing comma because it breaks IE.
    outlines.append("]")
    with open(outfile, 'w') as f:
        f.write('\n'.join(outlines) + '\n')


def main(infile, outfile, varname):
    """Usually should not need to change this method, but do so as needed."""
    print('Will create ' + outfile)
    print('Processing...')
    process(infile, outfile, varname)
    print('...success!')


if __name__ == '__main__':
    main(*sys.argv[1:])
