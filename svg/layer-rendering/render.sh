#! /bin/bash
# Create bitmaps for icons in 3 flavours from SVG files.
#
set -e

source ../svg2png.sh funcdef

if test -z "$1"; then
    echo "Usage: $0 [-n] <widths>"
    exit 1
fi

DRY_RUN=""
if test "$1" = "-n"; then
    DRY_RUN="echo "
    shift
fi

#set -x

find . -name '*.svg' | while read svg_file; do
    svg2png "$svg_file" --layer 1 square  "$@"
    svg2png "$svg_file" --layer 2 rounded "$@"
    svg2png "$svg_file" --layer 3 circle  "$@"
done
