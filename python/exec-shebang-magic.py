#!/bin/sh
""":"
echo "Hi, this is $SHELL!"
exec /usr/bin/python3 "$0" "$@"
:

The doc string, not seen by ``sh``.
"""
import sys

__doc__ = __doc__.split('\n:\n', 1)[1].strip()

print("Hello from Python {}!".format(sys.version.split()[0]))
print(__doc__)
