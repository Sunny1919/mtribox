#!/bin/bash

ROOTFS_DIR="/home/container/arch-rootfs"
ARCH_URL="https://mirror.rackspace.com/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.gz"
PROOT_URL="https://github.com/proot-me/proot/releases/download/v5.3.0/proot-v5.3.0-x86-64-static"

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    curl -Lo /tmp/arch.tar.gz "$ARCH_URL"
    mkdir -p "$ROOTFS_DIR"
    tar -xzf /tmp/arch.tar.gz --strip-components=1 -C "$ROOTFS_DIR"
    
    mkdir -p "$ROOTFS_DIR/usr/local/bin"
    curl -Lo "$ROOTFS_DIR/usr/local/bin/proot" "$PROOT_URL"
    chmod 755 "$ROOTFS_DIR/usr/local/bin/proot"
    
    echo -e "nameserver 1.1.1.1\nnameserver 8.8.8.8" > "$ROOTFS_DIR/etc/resolv.conf"
    
    touch "$ROOTFS_DIR/.installed"
fi

"$ROOTFS_DIR/usr/local/bin/proot" \
--rootfs="$ROOTFS_DIR" \
--link2symlink \
--kill-on-exit \
--root-id \
--cwd=/root \
--bind=/proc \
--bind=/dev \
--bind=/sys \
--bind=/tmp \
/usr/bin/bash
