#!/bin/bash

ROOTFS_DIR="/home/container/arch-rootfs"
ARCH_URL="http://mirror.rackspace.com/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.gz"
PROOT_URL="https://github.com/proot-me/proot/releases/download/v5.3.0/proot-v5.3.0-x86-64-static"

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    echo "--- Đang tải Arch Linux (17GB RAM) ---"
    mkdir -p "$ROOTFS_DIR"
    curl -L "$ARCH_URL" -o /tmp/arch.tar.gz
    
    echo "--- Đang giải nén hệ thống ---"
    tar -xzf /tmp/arch.tar.gz --strip-components=1 -C "$ROOTFS_DIR"
    
    echo "--- Thiết lập PRoot ---"
    mkdir -p "$ROOTFS_DIR/usr/local/bin"
    mkdir -p "$ROOTFS_DIR/etc"
    curl -L "$PROOT_URL" -o "$ROOTFS_DIR/usr/local/bin/proot"
    chmod 755 "$ROOTFS_DIR/usr/local/bin/proot"
    
    printf "nameserver 1.1.1.1\nnameserver 8.8.8.8" > "$ROOTFS_DIR/etc/resolv.conf"
    touch "$ROOTFS_DIR/.installed"
fi

echo "--- ĐANG VÀO ARCH LINUX ---"
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
