import subprocess
import threading
import http.server
import socketserver
import re
import sys
import time
import webbrowser
import io
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def start_local_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"[Server Error] {e}")

def main():
    # 1. Start local server in background daemon thread
    server_thread = threading.Thread(target=start_local_server, daemon=True)
    server_thread.start()
    time.sleep(1.0)
    print("[OK] 로컬 웹 서버가 포트 8080에서 시작되었습니다.")

    # 2. Run cloudflared tunnel
    cloudflared_exe = DIRECTORY / "cloudflared.exe"
    if not cloudflared_exe.exists():
        print(f"[Error] {cloudflared_exe} 를 찾을 수 없습니다.")
        sys.exit(1)

    print("[*] Cloudflare 보안 터널을 생성하여 공개 HTTPS URL을 발급받는 중입니다...")
    cmd = [str(cloudflared_exe), "tunnel", "--url", f"http://localhost:{PORT}"]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    # Read output line by line to extract the URL
    for line in proc.stdout:
        print(line, end="", flush=True)
        match = url_pattern.search(line)
        if match:
            tunnel_url = match.group(0)
            break

    if tunnel_url:
        print("\n" + "=" * 70)
        print("🎉 [웹 연구 대시보드 외부 공개 배포 성공!]")
        print("=" * 70)
        print(f"🌐 인터넷 공개 HTTPS 주소 : {tunnel_url}")
        print(f"📌 로컬 내 컴퓨터 주소    : http://localhost:{PORT}")
        print("=" * 70)
        print("전 세계 누구나 위 HTTPS 링크를 통해 연구 대시보드에 즉시 접속할 수 있습니다.")
        print("이 프로세스가 동작하는 동안 외부 링크가 계속 유지됩니다.")

        # Save to file
        with open(DIRECTORY / "public_url.txt", "w", encoding="utf-8") as f:
            f.write(tunnel_url)

        # Open in browser
        if "--no-browser" not in sys.argv:
            webbrowser.open(tunnel_url)

        # Keep process alive
        try:
            for line in proc.stdout:
                pass
        except KeyboardInterrupt:
            print("\n터널을 종료합니다...")
            proc.terminate()
    else:
        print("[Error] Cloudflare 터널 URL을 발급받지 못했습니다.")
        proc.terminate()

if __name__ == "__main__":
    main()
