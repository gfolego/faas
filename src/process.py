#!/usr/bin/python


# process.py
# Copyright 2017
#     Bruno Ribeiro
#     Guilherme Folego (gfolego@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



# Definitions
START_STR='08:00'
END_STR='17:00'


import sys
import argparse


def parse_args(argv):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('infile', metavar='input.ps', type=argparse.FileType('r'),
                            help='input PostScript file')
    parser.add_argument('outfile', metavar='output.ps', type=argparse.FileType('w'),
                            help='output PostScript file')
    parser.add_argument('pos', metavar='position', type=float, nargs='+',
                            help='positions for time entries')
    parser.add_argument('-s', '--start', type=str, default=START_STR,
                            help='string to be used as start time')
    parser.add_argument('-e', '--end', type=str, default=END_STR,
                            help='string to be used as end time')
    parser.add_argument('-d', '--debug', action='store_true',
                            help='activate debug mode')

    args = parser.parse_args(args=argv)
    return args


def process(infile, outfile, pos,
        startstr=START_STR, endstr=END_STR,
        debug=False):

    content = infile.read()

    pos1 = content.find("COLABORADOR)Tj")
    pos2 = content.rfind("<</Length", 0, pos1);
    pos3 = content.find("endstream", pos1)

    # everything before the first page
    firstPart = content[:pos2]
    # everything after the first page
    lastPart  = content[pos3:]
    # first page data
    content   = content[pos2:pos3]
    # skip the 'start of stream' marker
    pos2 = content.find("stream")
    content = content[pos2 + 6:]

    extra = []
    # define the current font
    extra.append('/R12 9 Tf')

    # Note: at the point this extra content is inserted, the coordinate system is reset to its
    # default (i.e. origin is located at the bottom left corner of the page)

    # fix the y positions
    pos = [ y - 1 for y in pos ]

    # create PostScript entries using some dark magic
    for y in pos:
        # write the start time
        extra.append('68 ' + str(y) + ' moveto')
        extra.append('(' + startstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')
        # write the end time
        extra.append('186 ' + str(y) + ' moveto')
        extra.append('(' + endstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')

    # insert any extra content at the end of the stream (later content has higher z-index)
    pos1 = content.find('Q\nQ\n\n')
    content = content[:pos1 + 5] + '\n' + '\n'.join(extra) + '\n' + content[pos1 + 5:]

    outfile.write(firstPart)
    outfile.write("<</Length ")
    outfile.write(str(len(content)))
    outfile.write(">>stream\n")
    outfile.write(content)
    outfile.write(lastPart)


# Main
def main(argv):

    # Parse arguments
    args = parse_args(argv)
    if args.debug: print(args)

    process(args.infile, args.outfile, args.pos,
            args.start, args.end, args.debug)


if __name__ == "__main__":
    main(sys.argv[1:])

