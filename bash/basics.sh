#
# Basic helpers for any shell script
#
# You don't want a dependency for these, and they're pretty simple
# and stable, so just break the rules and cut'n'copy them.
#

fail() { # fail with error message on stderr and exit code 1
    echo >&2 "ERROR:" "$@"
    exit 1
}

