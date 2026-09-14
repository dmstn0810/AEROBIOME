import http.server
import socketserver
import socket
import sys
import webbrowser
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def main():
    local_ip = get_ip()
    print("=" * 65)
    print("🌲 건국대학교 괴산학술림 공기미생물·음이온 연구 대시보드 웹서버")
    print("=" * 65)
    print(f"📌 내 컴퓨터 접속 주소    : http://localhost:{PORT}")
    print(f"🌐 같은 Wi-Fi/네트워크 주소: http://{local_ip}:{PORT}")
    print("=" * 65)
    print("웹 서버가 백그라운드에서 동작 중입니다. (종료: Ctrl + C)")
    
    if "--no-browser" not in sys.argv:
        webbrowser.open(f"http://localhost:{PORT}")
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n웹 서버를 정상 종료합니다.")

if __name__ == "__main__":
    main()
