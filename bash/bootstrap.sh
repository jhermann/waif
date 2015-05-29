#!/usr/bin/env bash
#
# Fundamental host bootstrap for Debian and look-alikes, run as root
#

fail() { # fail with error message on stderr and exit code 1
    echo >&2 "ERROR:" "$@"
    exit 1
}

test $(id -u) -eq 0 || fail 'Run me as root!'

apt-get update
apt-get upgrade
apt-get install -y curl wget htop tmux
apt-get install -y build-essential git gitk
apt-get install -y python python-setuptools python-pkg-resources python-virtualenv python-pip python-dev

mkdir -p /root/.ssh
chmod 700 /root/.ssh
touch /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

cat >/etc/profile.d/aliases.sh <<'.'
alias ..="cd .."
alias ...="cd ../.."
alias dir="ls -F"
alias l="ls -l"
alias ll="ls -l"
alias la="ls -la"
alias md=mkdir
.
