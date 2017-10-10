#!/bin/bash


# faas.sh
# Copyright 2017 Guilherme Folego (gfolego@gmail.com)
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



###################
### Definitions ###
###################

# "1" for debug
DEBUG="0"



##################
### Parse args ###
##################

# Check input parameters

if [[ $# -ne 2 ]] ; then
    echo "Usage: faas.sh <input.pdf> <output.pdf>"
    exit 1
fi

infile="$1"
outfile="$2"


if [[ ! -f "$infile" ]] ; then
    echo "File $infile not found."
    exit 1
fi


if [[ "$infile" != *.pdf ]] || [[ $(file --mime-type -b "$infile") != application/pdf ]] ; then
    echo "File $infile is not a PDF."
    exit 1
fi


if [[ "$outfile" != *.pdf ]] ; then
    echo "File $outfile is not a PDF."
    exit 1
fi

outdir=$(dirname "$outfile")
if [[ $(mkdir -p "$outdir") ]] ; then
    echo "Unable to create directory $outdir"
    exit 1
fi


# Temporary directory for temporary files
tmpdir=$(mktemp -d)
if [[ $? -ne 0 ]] ; then
    echo "Unable to create temporary directory $tmpdir"
    exit 1
fi
[[ "$DEBUG" == "1" ]] && echo "Temp dir: $tmpdir"


# Source directory
srcdir="$(dirname "$0")/"
[[ "$DEBUG" == "1" ]] && echo "Src bir: $srcdir"




############
### Main ###
############


echo -e "Processing started\nThis may take a minute..."


# Calculate pdf size (height)
size=$(pdfinfo "$infile" | grep "^Page size:" | sed -e s,.*x\ ,, -e s,\ .*,,)
[[ "$DEBUG" == "1" ]] && echo "Size: $size"

# Calculate entries positions
pos=($(pdftotext "$infile" -bbox /dev/stdout |
		grep ">-----</word>" -B1 |
		grep ">[0-9][0-9]</word>" |
		cut -f4,8 -d\" | sed s,\",+, | bc |
		xargs -i echo "$size"-{}*0.5 | bc ))
[[ "$DEBUG" == "1" ]] && printf "Pos: %s\n" "${pos[@]}"

# Process
inputps="$tmpdir"/input.ps
outputps="$tmpdir"/output.ps

pdf2ps "$infile" "$inputps"
python "$srcdir"/process.py "$inputps" "$outputps" "${pos[@]}"
ps2pdf "$outputps" "$outfile"

# Clean up
[[ "$DEBUG" != "1" ]] && rm -rf "$tmpdir"

echo "Success generating $outfile"

