DRY_RUN=false

guarded_append() {
    # Append stdin to file $1 if the regex $2 doesn't appear in it.
    file="$1"
    regex="$2"

    if grep "$regex" "$file" >/dev/null; then
        trace "File $file already contains '$regex'"
        cat >>/dev/null
    else
        if $DRY_RUN; then
            info "DRY RUN: File $file would be appended with '$regex'"
            cat >>/dev/null
        else
            info "File $file appended with '$regex'"
            cat >>"$file"
        fi
    fi
}

