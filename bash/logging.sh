#
# Logging / diagnostics
#
ESC=$(echo -en \\0033)
BOLD="$ESC[1m"
OFF="$ESC[0m"

# Show traces?
DEBUG=true


bold() {
    echo "$BOLD""$@""$OFF"
}

banner() { # e.g. banner "~" "Title"
    local ch
    ch="$1"; shift
    for i in $(seq 78); do echo -n "$ch"; done; echo
    echo -n "$ch "
    bold "$@"
    for i in $(seq 78); do echo -n "$ch"; done; echo
}

trace() {
    $DEBUG && echo "TRACE: ""$@" || :
}

info() {
    echo "INFO:" "$@"
}

warn() {
    bold "WARN:" "$@"
}

fail() {
    trap ERR
    bold "FATAL ERROR:" "$@"
    exit 1
}

error_trap() {
    RC=$?
    trap ERR
    bold "FAILURE: Premature end of script with RC=$RC, read the log!"
    exit $RC
}

# Register failure TRAP
trap error_trap ERR

