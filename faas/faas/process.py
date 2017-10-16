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
FMT_STR='%H:%M'

# PostScript definitions
PS_GRAY_DARK = '.2 setgray'
PS_GRAY_LIGHT = '.5 setgray'
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

import subprocess
import os

from datetime import datetime, timedelta
import random


def parse_args(argv):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('infile', metavar='input.pdf', type=str,
                            help='input PDF file')
    parser.add_argument('outfile', metavar='output.pdf', type=str,
                            help='output PDF file')
    parser.add_argument('-s', '--start', type=str, default=START_STR,
                            help='string to be used as start time')
    parser.add_argument('-e', '--end', type=str, default=END_STR,
                            help='string to be used as end time')
    parser.add_argument('-v', '--variation', type=int, default=0,
                            help='random variation in minutes')
    parser.add_argument('--dashed', action='store_true',
                            help='put a dash in the signature for non-working days')
    parser.add_argument('-d', '--debug', action='store_true',
                            help='activate debug mode')

    args = parser.parse_args(args=argv)
    return args


def randomize_hours(startstr=START_STR, endstr=END_STR, variation=0):
    variation = abs(variation)
    rnd = random.randint(-variation, +variation)
    rnd_dt = timedelta(minutes=rnd)

    start = datetime.strptime(startstr, FMT_STR) + rnd_dt
    end = datetime.strptime(endstr, FMT_STR) + rnd_dt

    randstartstr = start.strftime(FMT_STR)
    randendstr = end.strftime(FMT_STR)

    return randstartstr, randendstr


def process_ps(infile, outfile, slots,
        startstr=START_STR, endstr=END_STR,
        variation=0,
        dashed=False, debug=False):

    with open(infile) as f:
        content = f.read()

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
            randstartstr, randendstr = randomize_hours(startstr, endstr, variation)

            # write the start time
            extra.append(PS_GRAY_DARK)
            extra.append(str(PS_START_CENTER_X) + ' ' + str(y) + ' moveto')
            extra.append('(' + randstartstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')
            # write the end time
            extra.append(PS_GRAY_DARK)
            extra.append(str(PS_END_CENTER_X) + ' ' + str(y) + ' moveto')
            extra.append('(' + randendstr + ') dup stringwidth pop 2 div neg 0 rmoveto show')
            # write a dot in the signature if the dash is disabled
            if not dashed:
                extra.append('newpath')
                extra.append(str(PS_SIGNATURE_X + PS_DOT_OFFSET)     + ' ' + str(y - 2) + ' moveto')
                extra.append(str(PS_SIGNATURE_X + PS_DOT_OFFSET + 1) + ' ' + str(y - 2) + ' lineto')
                extra.append('1 setlinewidth')
                extra.append(PS_GRAY_LIGHT)
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

    with open(outfile, 'w') as f:
        f.write(firstPart)
        f.write("<</Length ")
        f.write(str(len(content)))
        f.write(">>stream\n")
        f.write(content)
        f.write(lastPart)


def coordinates2slots(pos):
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


# Return time positions (originally written in Bash)
# We know "shell=True" is less than ideal -- contributions welcome!
def find_positions(infile):
    size = subprocess.check_output(
        'pdfinfo "%s" | grep "^Page size:" | sed -e s,.*x\ ,, -e s,\ .*,,' % infile,
        shell=True).rstrip('\n')

    pos = subprocess.check_output(
	'pdftotext "%s" -bbox /dev/stdout | '
	'grep ">-----</word>" -B1 | '
	'grep ">[0-9][0-9]</word>" | '
	'cut -f4,8 -d\\" | sed s,\\",+, | bc | '
	'xargs -i echo "%s"-{}*0.5 | bc' % (infile, size),
	shell=True).rstrip('\n').splitlines()

    pos = [float(i) for i in pos]

    if len(pos) == 0:
        raise RuntimeError('Error processing PDF')

    return pos


def pipeline(infile, outfile,
        start=START_STR, end=END_STR,
        variation=0,
        dashed=False, debug=False):

    # Find positions
    pos = find_positions(infile)

    # find out which days are working days
    slots = coordinates2slots(pos)

    # Convert PDF to PS
    ps_infile = os.path.join(os.path.dirname(outfile), 'infile.ps')
    ps_outfile = os.path.join(os.path.dirname(outfile), 'outfile.ps')
    out = subprocess.check_output(['pdf2ps', infile, ps_infile], stderr=subprocess.STDOUT)
    if out != "":
        raise RuntimeError('Error processing PDF')

    # generate a new PostScript file
    process_ps(ps_infile, ps_outfile, slots,
            start, end, variation, dashed, debug)

    # Convert PS to PDF
    out = subprocess.check_output(['ps2pdf', ps_outfile, outfile], stderr=subprocess.STDOUT)
    if out != "":
        raise RuntimeError('Error processing PDF')

    # Cleanup
    os.unlink(ps_infile)
    os.unlink(ps_outfile)


# Main
def main(argv):

    # Parse arguments
    args = parse_args(argv)
    if args.debug: print(args)

    pipeline(args.infile, args.outfile,
            args.start, args.end, args.variation,
            args.dashed, args.debug)


if __name__ == "__main__":
    main(sys.argv[1:])

