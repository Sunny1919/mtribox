import os, subprocess, urllib.request, tarfile, shutil

# --- Cấu hình ví ---
LTC_WALLET = "LTC:ltc1q4dr0ast2umy5cqrckg877vsatt2t5c5n4p0r3v.PteroXeon"
ETH_WALLET = "ETH:0xF09Bd9E017dd09aa7F56aeE15c90335207d34618.PteroXeon"

XMR_URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
NBM_URL = "https://github.com/NebuTech/NBMiner/releases/download/v42.3/NBMiner_42.3_Linux.tgz"

def setup_direct():
    # 1. Tối ưu hệ thống (Huge Pages)
    print("[*] Tối ưu hóa Huge Pages...")
    subprocess.run(["sudo", "sysctl", "-w", "vm.nr_hugepages=2560"])

    # 2. Tải và cài đặt XMRig
    if not os.path.exists("xmrig_bin"):
        print("[*] Đang cài đặt XMRig...")
        urllib.request.urlretrieve(XMR_URL, "xmrig.tar.gz")
        with tarfile.open("xmrig.tar.gz", "r:gz") as tar:
            tar.extractall(path="xmrig_temp")
        # Tìm file thực thi
        for root, dirs, files in os.walk("xmrig_temp"):
            if "xmrig" in files:
                shutil.move(os.path.join(root, "xmrig"), "xmrig_bin")
                break
        os.chmod("xmrig_bin", 0o755)
        shutil.rmtree("xmrig_temp")
        os.remove("xmrig.tar.gz")

    # 3. Tải và cài đặt NBMiner
    if not os.path.exists("nbminer_bin"):
        print("[*] Đang cài đặt NBMiner...")
        urllib.request.urlretrieve(NBM_URL, "nbminer.tgz")
        with tarfile.open("nbminer.tgz", "r:gz") as tar:
            tar.extractall(path="nbminer_temp")
        for root, dirs, files in os.walk("nbminer_temp"):
            if "nbminer" in files:
                shutil.move(os.path.join(root, "nbminer"), "nbminer_bin")
                break
        os.chmod("nbminer_bin", 0o755)
        shutil.rmtree("nbminer_temp")
        os.remove("nbminer.tgz")

def run_mining():
    print("[*] Đang khởi chạy đào trực tiếp (CPU + GPU)...")
    
    # Chạy NBMiner (GPU) dưới nền
    nbm_cmd = [
        "./nbminer_bin", "-a", "ethash", 
        "-o", "stratum+tcp://ethash.unmineable.com:3333", 
        "-u", ETH_WALLET, "-d", "0,1,2,3", "-log"
    ]
    subprocess.Popen(nbm_cmd)
    
    print("[*] GPU Miner đã chạy ngầm. Đang khởi chạy CPU Miner...")

    # Chạy XMRig (CPU) trực tiếp để xem log
    xmr_cmd = [
        "sudo", "./xmrig_bin", "-a", "rx/0", 
        "-o", "rx.unmineable.com:443", 
        "-u", LTC_WALLET, "--tls", 
        "--threads", "40", "--randomx-mode", "fast", "--cpu-priority", "5"
    ]
    subprocess.run(xmr_cmd)

if __name__ == "__main__":
    setup_direct()
    run_mining()
