#!/bin/bash

ROOTFS_DIR="/home/container/arch-rootfs"
ARCH_URL="http://mirror.rackspace.com/archlinux/iso/latest/archlinux-bootstrap-x86_64.tar.zst"
PROOT_URL="https://github.com/proot-me/proot/releases/download/v5.3.0/proot-v5.3.0-x86-64-static"
ZSTD_BIN="https://github.com/facebook/zstd/releases/download/v1.5.5/zstd-v1.5.5-linux-x86_64"

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    rm -rf "$ROOTFS_DIR"
    mkdir -p "$ROOTFS_DIR/usr/local/bin"
    mkdir -p "$ROOTFS_DIR/etc"

    # Tai truc tiep vao thu muc home de tranh loi /tmp day
    curl -L "$ARCH_URL" -o arch.tar.zst
    curl -L "$ZSTD_BIN" -o zstd_tmp
    chmod +x zstd_tmp
    
    # Giai nen va xoa ngay file nen de giai phong dung luong
    ./zstd_tmp -d arch.tar.zst -o arch.tar
    rm arch.tar.zst zstd_tmp
    
    tar -xf arch.tar --strip-components=1 -C "$ROOTFS_DIR"
    rm arch.tar
    
    curl -L "$PROOT_URL" -o "$ROOTFS_DIR/usr/local/bin/proot"
    chmod 755 "$ROOTFS_DIR/usr/local/bin/proot"
    
    printf "nameserver 1.1.1.1\nnameserver 8.8.8.8" > "$ROOTFS_DIR/etc/resolv.conf"
    
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
