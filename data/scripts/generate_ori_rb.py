"""Generates a Ruby file that contains police ORI data."""

import sys

import pandas as pd


def process(infile, outfile):
    """Read data from infile and generate Ruby at outfile."""
    outlines = [
        "# This file was automatically generated by a rule in the Makefile",
        "module Constants",
        "  DEPARTMENT_BY_ORI = {",
    ]

    df = pd.read_csv(infile)
    for name, ori in zip(df['AGENCY_NAME'], df['ORI']):
        outlines.append('    "%s" => "%s",' % (ori, name))

    outlines[-1] = outlines[-1][:-1]
    outlines.extend([
        "  }.freeze",
        "end"
    ])
    with open(outfile, 'w') as f:
        f.write('\n'.join(outlines) + '\n')


def main(infile, outfile):
    """Usually should not need to change this method, but do so as needed."""
    print('Creating {} ...'.format(outfile))
    process(infile, outfile)
    print('...success!')


if __name__ == '__main__':
    main(*sys.argv[1:])
