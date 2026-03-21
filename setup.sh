#!/bin/bash

ROOTFS_DIR="/home/container/arch-rootfs"
ARCH_URL="http://mirror.rackspace.com/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.zst"
PROOT_URL="https://github.com/proot-me/proot/releases/download/v5.3.0/proot-v5.3.0-x86_64-static"
ZSTD_BIN="https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-linux-x86_64"

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    rm -rf "$ROOTFS_DIR"
    mkdir -p "$ROOTFS_DIR/usr/local/bin"
    mkdir -p "$ROOTFS_DIR/etc"

    curl -L "$ARCH_URL" -o /tmp/arch.tar.zst
    curl -L "$ZSTD_BIN" -o /tmp/zstd
    chmod +x /tmp/zstd
    
    /tmp/zstd -d /tmp/arch.tar.zst -o /tmp/arch.tar
    tar -xf /tmp/arch.tar --strip-components=1 -C "$ROOTFS_DIR"
    
    curl -L "$PROOT_URL" -o "$ROOTFS_DIR/usr/local/bin/proot"
    chmod 755 "$ROOTFS_DIR/usr/local/bin/proot"
    
    printf "nameserver 1.1.1.1\nnameserver 8.8.8.8" > "$ROOTFS_DIR/etc/resolv.conf"
    
    rm -rf /tmp/arch.tar.zst /tmp/arch.tar /tmp/zstd
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
