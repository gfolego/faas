#!/bin/bash



###################
### Definitions ###
###################

# "1" for debug
DEBUG="0"

# Offset for pdfjam
OFFSET8="-225"
OFFSET1="-115"
OFFSET7="-108"

# Scale for pdfjam
SCALE8="0.035"
SCALE1="0.03"
SCALE7="0.03"



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


# Resources directory
resdir="$(dirname "$0")/../res"
[[ "$DEBUG" == "1" ]] && echo "Res bir: $resdir"




############
### Main ###
############


echo -e "Processing started\nThis may take a minute..."


# Calculate pdf size (height)
size=$(pdfinfo "$infile" | grep "^Page size:" | sed -e s,.*x\ ,, -e s,\ .*,,)
[[ "$DEBUG" == "1" ]] && echo "Size: $size"

# Calculate entries positions
pos=($(pdftotext "$infile" -bbox /dev/stdout | grep ">-----</word>" -B1 | grep ">[0-9][0-9]</word>" | cut -f4,8 -d\" | sed s,\",+, | bc | xargs -i echo "$size"*0.5-{}*0.5 | bc ))
[[ "$DEBUG" == "1" ]] && printf "Pos: %s\n" "${pos[@]}"


# Create a PDF for each entry
for i in ${!pos[@]}; do
    pdfjam --quiet --scale "$SCALE8" --offset "$OFFSET8 ${pos[i]}" "$resdir"/8.pdf --outfile "$tmpdir"/jam8-"$i".pdf
    pdfjam --quiet --scale "$SCALE1" --offset "$OFFSET1 ${pos[i]}" "$resdir"/1.pdf --outfile "$tmpdir"/jam1-"$i".pdf
    pdfjam --quiet --scale "$SCALE7" --offset "$OFFSET7 ${pos[i]}" "$resdir"/7.pdf --outfile "$tmpdir"/jam7-"$i".pdf
done

# Separate input pages
pdftk "$infile" cat 1 output "$tmpdir"/stamp-0.pdf
pdftk "$infile" cat 2 output "$tmpdir"/back.pdf

# Combine entries
for i in ${!pos[@]}; do
    pdftk "$tmpdir"/jam8-"$i".pdf  stamp "$tmpdir"/jam1-"$i".pdf   output "$tmpdir"/tmp-"$i".pdf
    pdftk "$tmpdir"/tmp-"$i".pdf   stamp "$tmpdir"/jam7-"$i".pdf   output "$tmpdir"/jamall-"$i".pdf
    pdftk "$tmpdir"/stamp-"$i".pdf stamp "$tmpdir"/jamall-"$i".pdf output "$tmpdir"/stamp-"$((i+1))".pdf
done

# Generate final file
pdfunite "$tmpdir"/stamp-${#pos[@]}.pdf "$tmpdir"/back.pdf "$outfile"

# Clean up
rm -rf "$tmpdir"

echo "Success generating $outfile"

