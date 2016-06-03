#! /bin/bash
# Create bitmaps from SVG files.
#
# Converts all SVG files in the current directory according
# to passed parameters:
#
#       -n: dry run option (just show the commands).
#
#       --layer n name: select the ‹n›th layer below the top one,
#               delete the others (for ‹n›=1…3); the ‹name› is
#               used as part of the rendered PNG file.
#
#       positional arguments: widths of the rendered PNGs.
#
# File dates are used to skip already rendered images.
#
# To use this as a function library, source it:
#
#       source svg2png.sh funcdef
#
set -e

use_xvfb=true
inkscape=/usr/bin/inkscape
log=/tmp/$(basename "$0")"-xvfb.log"
DRY_RUN=""

if $use_xvfb; then
    command which xvfb-run >/dev/null || { echo 'Please execute "sudo aptitude install xvfb"!'; exit 1; }
fi

_svg2png_mtime() {
    test -e "$1" && stat --format "%Y" "$1" || echo "0"
}

_svg2png_usage() {
    echo "Usage: $0 [-n] [--layer # name] <width>..."
    test -z "$1" || echo "$@"
    exit 1
}

svg2png() {
    local svg_file="$1"; shift
    local inkscape_opts=( )
    local name_traits=""

    while test "${1:0:1}" = '-'; do
        case "$1" in
            --layer)
                name_traits="${name_traits}_$3"
                inkscape_opts+=( --verb=LayerShowAll )
                for i in $(seq 1 3); do
                    inkscape_opts+=( --verb=LayerPrev )
                    test $i = $2 || inkscape_opts+=( --verb=LayerDelete )
                done
                inkscape_opts+=( --verb=FileSave --verb=FileQuit )
                shift; shift
                ;;
            *)
                _svg2png_usage "ERROR: Unknown option '$1'"
                ;;
        esac
        shift
    done

    svg_tmp="${svg_file}"
    test -z "$name_traits" || svg_tmp="/tmp/$USER-$(basename "${svg_file/%.svg/}")${name_traits}.svg"

    for width in $@; do
        png_file="${svg_file/%.svg/}${name_traits}_$width.png"
        if test $(_svg2png_mtime "$png_file") -lt $(_svg2png_mtime "$svg_file"); then
            if test ! -f "$svg_tmp"; then
                if $use_xvfb && test -z "$BUILD_URL"; then
                    xhost +localhost >/dev/null
                    xhost +$(hostname -f) >/dev/null
                fi
                cp "$svg_file" "$svg_tmp"
                if $use_xvfb; then
                    $DRY_RUN xvfb-run -a -n 42 -s " -extension RANDR " -e "$log" \
                        $inkscape -g -f "$svg_tmp" "${inkscape_opts[@]}"
                else
                    $DRY_RUN >>"$log" \
                        $inkscape -g -f "$svg_tmp" "${inkscape_opts[@]}"
                fi
            fi
            $DRY_RUN $inkscape -z -w $width -e "$png_file" "$svg_tmp"
        fi
    done

    test "$svg_tmp" = "$svg_file" || $DRY_RUN rm -- "$svg_tmp" 2>/dev/null || :
}

if test "$1" = "funcdef"; then
    return 0
fi

test -n "$1" || _svg2png_usage

if test "$1" = "-n"; then
    DRY_RUN="echo "
    shift
fi

#set -x

find . -name '*.svg' | while read svg_file; do
    svg2png "$svg_file" "$@"
done
