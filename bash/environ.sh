prependpathvar() {
    # get path variable given as first parameter and remove the
    # path given in the 2nd parameter, then re-add it in front
    # of all other entries
    local tmppath
    tmppath=$(eval echo '$'$1)
    tmppath="$(echo $tmppath | sed -e "s:$2::" -e 's/::/:/')"
    tmppath="$2${tmppath:+:$tmppath}"
    test -d $2 && export $1=$tmppath
}


