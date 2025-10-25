<!-- omit from toc -->
# My Jellyfin Setup

*Contents*
- [Overview](#overview)
- [Hardware](#hardware)
- [Configuration](#configuration)
- [Setup](#setup)
- [Administration](#administration)

## Overview
I run Jellyfin on a mini PC that is my home server (details see below), usable via the local network.
The server process is managed by `docker compose`.

See [my gallery repo](https://github.com/jhermann/gallery?tab=readme-ov-file#jellyfin)
for some custom artwork.

## Hardware

Homeserver:

* Beelink S12 Mini PC
* Intel 12th Gen (Alder Lake) Processor N100 (4C/4T, up to 3.4Ghz)
* 16G DDR4 • 500G PCIe SSD • 25W TDP
* 4K@60Hz Intel UHD dual HDMI 2.0
* LAN 1000M • Wifi 6 (2.4G + 5.8G dual-band 802.11ax) • BT5.2
* 4 × USB 3.2
* D/W/H 4.01 × 4.52 × 1.54 in
* OS: Linux Mint 21.2 Victoria
* Cost: About €200 in 2023

I use diverse clients in the form of Android tablet and phone,
Android TV (Firestick, beamer),
and the web client on my desktop.

## Configuration

The server runs in a docker container, managed by `docker-compose`.
Note that the main library folders for audio and video are mapped into the host filesystem,
so they can be moved if needed, without extensive reindexing.

`/srv/svc/jellyfin/docker-compose.yml`

```yaml
version: '3.5'
services:
  jellyfin:
    container_name: jellyfin
    image: jellyfin/jellyfin
    # sync with `id jellyfin`
    user: 128:1001
    network_mode: 'host'
    volumes:
      - ./config:/config
      - ./cache:/cache
      - /mnt/data/Audio:/media-audio
      - /mnt/data/Video:/media-video
      # - /path/to/media2:/media2:ro
    restart: 'unless-stopped'
    # Optional - alternative address used for autodiscovery
    environment:
      - JELLYFIN_PublishedServerUrl=http://home.fritz.box:8096/
    # Optional - may be necessary for docker health check to pass if running in host network mode
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

## Setup

To prepare your system, you need to `sudo apt install docker.io docker-compose`.

Setup as `root`:
```sh
docker pull jellyfin/jellyfin  # docker.io/jellyfin/jellyfin:latest
mkdir -p /srv/svc/jellyfin/{cache,config/log}
addgroup multimedia
adduser jellyfin --ingroup multimedia --home /srv/svc/jellyfin --system --disabled-password
chown -R jellyfin:multimedia ~jellyfin/
ln -nfs /srv/svc/jellyfin/config /etc/jellyfin  # make config more accessible
ln -nfs config/log /srv/svc/jellyfin/log  # make logs more visible
```

## Administration

Start:<br />
`cd /srv/svc/jellyfin; docker-compose up --detach`

Docker compose (re-)start:<br />
`cd /srv/svc/jellyfin; docker-compose down ; docker-compose up -d`

Docker compose logs:<br />
`cd /srv/svc/jellyfin; docker-compose logs -f`

Server update (check for necessary plugin updates afterwards):
```sh
cd /srv/svc/jellyfin; docker-compose down
docker pull jellyfin/jellyfin:latest
docker-compose up -d
```
