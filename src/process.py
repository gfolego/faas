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

# PostScript definitions
PS_GRAY_DARK = '.4 setgray'
PS_GRAY_LIGHT = '.8 setgray'
PS_START_CENTER_X = 68
PS_END_CENTER_X = 186
PS_SIGNATURE_X = 418
PS_SIG_CENTER_X = 418 + 154 / 2
PS_DASH_W = 100
PS_DOT_OFFSET = 5
PS_TABLE_CELL_Y = 18.78
PS_TABLE_OFFSET = 718.78


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
    parser.add_argument('--dashed', action='store_true',
                            help='put a dash in the signature for non-working days')
    parser.add_argument('-d', '--debug', action='store_true',
                            help='activate debug mode')

    args = parser.parse_args(args=argv)
    return args


def process(infile, outfile, slots,
        startstr=START_STR, endstr=END_STR,
        dashed=False, debug=False):

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

    # create PostScript entries using some dark magic
    for i in range(0, len(slots)):
        y = PS_TABLE_OFFSET - i * PS_TABLE_CELL_Y
        if slots[i]:
            # write the start time
            extra.append(PS_GRAY_DARK)
            extra.append(str(PS_START_CENTER_X) + ' ' + str(y) + ' moveto')
            extra.append('(' + startstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')
            # write the end time
            extra.append(PS_GRAY_DARK)
            extra.append(str(PS_END_CENTER_X) + ' ' + str(y) + ' moveto')
            extra.append('(' + endstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')
            # write a dot in the signature if the dash is disabled
            if not dashed:
                extra.append('newpath')
                extra.append(str(PS_SIGNATURE_X + PS_DOT_OFFSET)     + ' ' + str(y + 2) + ' moveto')
                extra.append(str(PS_SIGNATURE_X + PS_DOT_OFFSET + 1) + ' ' + str(y + 2) + ' lineto')
                extra.append('1 setlinewidth')
                extra.append(PS_GRAY_DARK)
                extra.append('stroke')
        elif dashed:
            # write a dash in the signature slot
            extra.append('newpath')
            extra.append(str(PS_SIG_CENTER_X - PS_DASH_W / 2) + ' ' + str(y + 2) + ' moveto')
            extra.append(str(PS_SIG_CENTER_X + PS_DASH_W / 2) + ' ' + str(y + 2) + ' lineto')
            extra.append('.5 setlinewidth')
            extra.append(PS_GRAY_LIGHT)
            extra.append('stroke')

    # insert any extra content at the end of the stream (later content has higher z-index)
    pos1 = content.find('Q\nQ\n\n')
    content = content[:pos1 + 5] + '\n' + '\n'.join(extra) + '\n' + content[pos1 + 5:]

    outfile.write(firstPart)
    outfile.write("<</Length ")
    outfile.write(str(len(content)))
    outfile.write(">>stream\n")
    outfile.write(content)
    outfile.write(lastPart)


def coordinatesToSlots(pos):
    """ Return a boolean list indicating which slots are in use """

    slots = [ False for i in range(0, 31)]
    offset = PS_TABLE_OFFSET + PS_TABLE_CELL_Y / 2
    j = 0
    for i in range(0, len(slots)):
        offset -= PS_TABLE_CELL_Y
        if pos[j] > offset:
            slots[i] = True
            j += 1
        else:
            slots[i] = False

        if len(pos) <= j: break

    return slots


# Main
def main(argv):

    # Parse arguments
    args = parse_args(argv)
    if args.debug: print(args)

    # find out which days are working days
    slots = coordinatesToSlots(args.pos)
    # generate a new PostScript file
    process(args.infile, args.outfile, slots,
            args.start, args.end, args.dashed, args.debug)


if __name__ == "__main__":
    main(sys.argv[1:])

