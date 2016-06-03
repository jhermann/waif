SVG Tricks
==========

This directory contains a collection of small helpers for
working with SVG files, mainly using `Inkscape`_,
`ImageMagick`_, and *bash*.


General Tools
-------------

The ``svg2png.sh`` script converts all SVG files in the current directory according
to passed parameters. It can also be used as a *bash* function library. See the
script for details.


Layer Rendering
---------------

The ``layer-rendering`` sub-directory contains an example of
an icon with square, rounded, and circular backgrounds placed
in layers, below a layer with the foreground motive.
A *bash* script renders that icon in its three versions to PNG,
at a set size.


.. _`Inkscape`: https://inkscape.org/en/
.. _`ImageMagick`: http://www.imagemagick.org/
